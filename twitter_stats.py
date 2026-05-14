#!/usr/bin/env python3
"""
Gin 日志 IP 统计 — 解析 [GIN] 日志，按日统计独立 IP 与真实活跃用户。

用法:
    python3 twitter_stats.py <logfile> [options]
    python3 twitter_stats.py nohup.out
    python3 twitter_stats.py nohup.out.gz --max-items 200

真实活跃用户判断:
    漫画站 / 图站 (默认):
    - 强信号: 访问带了 ?host= 或 ?proxy_host= 的页面 → 必真人
    - 同一漫画 (/s/HASH/NUM) 内的顺序翻页 → 真人阅读行为
    - 同一漫画内乱序访问过多 (>50%) → 爬虫嫌疑
    - 访问漫画数 > --max-items → 批量抓取

    API 站 (--mode api):
    - 多种请求类型 + 合理请求量
"""

import argparse
import gzip
import json
import os
import re
import sys
from collections import defaultdict

LINE_RE = re.compile(
    r'\[GIN\] (\d{4}/\d{2}/\d{2}) - \d{2}:\d{2}:\d{2} '
    r'\| \d+ \| .+? \|\s+([\d.a-fA-F:]+) \| (\w+)\s+"([^"]*)"'
)

STATIC_EXTS = {'.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg',
               '.ico', '.woff', '.woff2', '.ttf', '.eot', '.map',
               '.webp', '.avif', '.json', '.xml', '.txt', '.wasm'}

# /s/HASH/NUM → 提取 hash 和页码
S_RE = re.compile(r'^/s/([a-f0-9]+)/(\d+)-(\d+)$')
G_RE = re.compile(r'^/g/(\d+)/')


def is_static(path: str) -> bool:
    _, ext = os.path.splitext(path.split('?')[0])
    return ext.lower() in STATIC_EXTS


def has_human_signal(raw_path: str) -> bool:
    """真人强信号: ?host= 或 ?proxy_host="""
    return '?host=' in raw_path or '?proxy_host=' in raw_path


def classify(path: str) -> str:
    """页面类型"""
    clean = path.split('?')[0].rstrip('/') or '/'

    if clean == '/':
        qs = path.split('?', 1)[1] if '?' in path else ''
        if any(k in qs for k in ('f_search=', 'f_cats=', 'next=')):
            return 'search'
        return 'home'

    if clean in ('/popular', '/misc', '/watched', '/cosplay'):
        return 'browse'

    if '/tag/' in clean:
        return 'browse'

    if '/s/' in clean or '/g/' in clean:
        return 'content'

    if '/uploader/' in clean:
        return 'browse'

    if '/torrent/' in clean or clean == '/gallerytorrents.php':
        return 'torrent'

    if '/api/' in clean:
        return 'api'

    if '/ext_tw_video/' in clean or '/amplify_video/' in clean:
        return 'video'

    return 'other'


def parse_s_page(path: str) -> tuple[str, int] | None:
    """解析 /s/HASH/NUM-PAGE 返回 (hash, page_num) 或 None"""
    m = S_RE.match(path)
    if m:
        return (m.group(1), int(m.group(3)))
    return None


def is_real_user_comic(rec: dict, max_items: int) -> bool:
    """
    漫画站真实用户判断:
    - 访问不同漫画太多 (>max_items) → 批量抓取 (不论有无host信号)
    - ?host= / ?proxy_host= 视为有浏览行为
    - 有浏览行为 + 看漫画 → 真人
    - 直接看漫画但顺序阅读 → 真人
    """
    types = rec['types']
    items = rec['items']
    unique_paths = rec['unique_paths']

    # 批量抓取: 无论什么信号，一天看几千部漫画不可能是真人
    if items > max_items:
        return False

    # 至少有过一些互操作
    if unique_paths < 2:
        return False

    # 真人强信号视为有浏览行为
    has_browse = bool(types & {'home', 'search', 'browse'}) or rec['has_human_signal']
    has_content = 'content' in types

    if has_browse and has_content:
        return True

    if has_browse and len(types) >= 2:
        return True

    # 直接访问漫画内容 (外部链接进来):
    # 看≥2部漫画 → 真人; 只看1部但顺序阅读 → 真人
    if has_content:
        if items >= 2:
            return True
        if rec.get('sequential_ratio', 0) > 0.5:
            return True
        if unique_paths <= 3:
            return True

    return False


def is_real_user_api(rec: dict, max_reqs: int) -> bool:
    """API 站真实用户: 合理请求量 + 多种类型 + 有数据下载"""
    if rec['reqs'] > max_reqs:
        return False
    if rec['unique_paths'] < 2:
        return False
    if len(rec['types']) < 2:
        return False
    if 'data' not in rec['types']:
        return False
    return True


def parse_log(filepath: str):
    """返回 {date: {ip: {各种统计字段}}}"""
    # date → ip → {reqs, paths, types, items_set, pages_by_hash, has_human_signal}
    daily = defaultdict(lambda: defaultdict(
        lambda: {'reqs': 0, 'paths': set(), 'types': set(),
                 'items_set': set(), 'pages_by_hash': defaultdict(list),
                 'has_human_signal': False}))

    opener = gzip.open if filepath.endswith('.gz') else open

    with opener(filepath, 'rt', encoding='utf-8', errors='ignore') as fh:
        for i, line in enumerate(fh):
            if i % 2_000_000 == 0:
                print(f"  ... {i // 1_000_000}M", file=sys.stderr)
            m = LINE_RE.match(line.strip())
            if not m:
                continue
            date, ip, method, raw_path = m.group(1), m.group(2), m.group(3), m.group(4)
            path = raw_path.split('?')[0].rstrip('/') or '/'
            if is_static(path):
                continue

            rec = daily[date][ip]
            rec['reqs'] += 1
            rec['paths'].add(path)
            rec['types'].add(classify(raw_path))

            if has_human_signal(raw_path):
                rec['has_human_signal'] = True

            # 解析漫画页
            sp = parse_s_page(path)
            if sp:
                hsh, page = sp
                rec['items_set'].add(f's:{hsh}')
                rec['pages_by_hash'][hsh].append(page)

            # 解析画廊
            gm = G_RE.match(path)
            if gm:
                rec['items_set'].add(f'g:{gm.group(1)}')

    # 计算统计字段
    result = {}
    for date, ips in daily.items():
        result[date] = {}
        for ip, d in ips.items():
            # 计算顺序阅读比例
            seq_pairs = 0
            total_pairs = 0
            for hsh, pages in d['pages_by_hash'].items():
                if len(pages) < 2:
                    continue
                for j in range(len(pages) - 1):
                    if pages[j] > 0:  # 有有效页码才计数
                        total_pairs += 1
                        if pages[j + 1] == pages[j] + 1:
                            seq_pairs += 1

            sequential_ratio = seq_pairs / max(total_pairs, 1)

            result[date][ip] = {
                'reqs': d['reqs'],
                'types': d['types'],
                'items': len(d['items_set']),
                'unique_paths': len(d['paths']),
                'has_human_signal': d['has_human_signal'],
                'sequential_ratio': sequential_ratio,
            }
    return result


def compute_stats(daily: dict, max_items: int, mode: str) -> dict:
    stats = {}
    for date in sorted(daily):
        ip_map = daily[date]
        total = len(ip_map)
        real = 0
        scraper = 0
        low_act = 0

        for d in ip_map.values():
            if mode == 'api':
                if is_real_user_api(d, max_items):
                    real += 1
                elif d['reqs'] > max_items:
                    scraper += 1
                else:
                    low_act += 1
            else:
                if is_real_user_comic(d, max_items):
                    real += 1
                elif d['items'] > max_items:
                    scraper += 1
                else:
                    low_act += 1

        stats[date] = {
            'total_unique_ips': total,
            'real_active_users': real,
            'high_req_bots': scraper,
            'low_activity': low_act,
        }
    return stats


def gen_html(stats: dict, title: str, out_path: str):
    data_json = json.dumps(stats)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#0f172a; color:#e2e8f0; min-height:100vh; }}
  .container {{ max-width:1200px; margin:0 auto; padding:2rem; }}
  h1 {{ text-align:center; font-size:1.8rem; margin-bottom:.5rem; color:#f1f5f9; }}
  .subtitle {{ text-align:center; color:#94a3b8; margin-bottom:2rem; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1rem; margin-bottom:2rem; }}
  .card {{ background:#1e293b; border:1px solid #334155; border-radius:12px; padding:1.3rem; text-align:center; }}
  .card .value {{ font-size:2rem; font-weight:700; }}
  .card .label {{ color:#94a3b8; font-size:.85rem; margin-top:.3rem; }}
  .chart-wrap {{ background:#1e293b; border:1px solid #334155; border-radius:12px; padding:1.5rem; margin-bottom:2rem; }}
  .chart-wrap h2 {{ font-size:1.1rem; margin-bottom:1rem; color:#cbd5e1; }}
  canvas {{ width:100%; }}
  table {{ width:100%; border-collapse:collapse; background:#1e293b; border-radius:12px; overflow:hidden; border:1px solid #334155; }}
  th {{ background:#334155; padding:.7rem 1rem; text-align:left; font-size:.8rem; text-transform:uppercase; letter-spacing:.05em; color:#94a3b8; }}
  td {{ padding:.55rem 1rem; border-top:1px solid #1e293b; font-size:.9rem; }}
  tr:hover td {{ background:rgba(255,255,255,.03); }}
  .pct {{ font-size:.8rem; color:#64748b; }}
  .footer {{ text-align:center; color:#475569; font-size:.78rem; margin-top:2rem; }}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p class="subtitle">每日 IP 访问统计 · 真实活跃用户 (host/proxy信号 + 顺序阅读 + 浏览行为)</p>

<div class="cards">
  <div class="card"><div class="value" style="color:#38bdf8;" id="totalDays">-</div><div class="label">统计天数</div></div>
  <div class="card"><div class="value" style="color:#4ade80;" id="avgTotal">-</div><div class="label">日均总 IP</div></div>
  <div class="card"><div class="value" style="color:#facc15;" id="avgReal">-</div><div class="label">日均真实用户</div></div>
  <div class="card"><div class="value" style="color:#ef4444;" id="avgBot">-</div><div class="label">日均爬虫/抓取</div></div>
  <div class="card"><div class="value" style="color:#f472b6;" id="avgPct">-</div><div class="label">平均真实占比</div></div>
</div>

<div class="chart-wrap">
  <h2>每日趋势</h2>
  <canvas id="chart" height="280"></canvas>
</div>

<div class="chart-wrap" style="overflow-x:auto;">
  <h2>每日明细</h2>
  <table id="table">
    <thead><tr><th>日期</th><th>总 IP</th><th>真实活跃</th><th>爬虫/抓取</th><th>低活跃</th><th>真实占比</th></tr></thead>
    <tbody></tbody>
  </table>
</div>

<p class="footer">Source: {os.path.basename(out_path)} · Generated <span id="genTime"></span></p>
</div>

<script>
const stats = {data_json};

const dates = Object.keys(stats);
const totalIps = dates.map(d => stats[d].total_unique_ips);
const realUsers = dates.map(d => stats[d].real_active_users);
const highBots = dates.map(d => stats[d].high_req_bots);
const lowAct = dates.map(d => stats[d].low_activity);

document.getElementById('totalDays').textContent = dates.length;
document.getElementById('avgTotal').textContent = Math.round(totalIps.reduce((a,b)=>a+b,0)/dates.length);
document.getElementById('avgReal').textContent = Math.round(realUsers.reduce((a,b)=>a+b,0)/dates.length);
document.getElementById('avgBot').textContent = Math.round(highBots.reduce((a,b)=>a+b,0)/dates.length);
const avgPct = realUsers.reduce((a,b,i)=>a + (b/totalIps[i]*100), 0)/dates.length;
document.getElementById('avgPct').textContent = avgPct.toFixed(1) + '%';
document.getElementById('genTime').textContent = new Date().toLocaleString('zh-CN');

new Chart(document.getElementById('chart'), {{
  type: 'line',
  data: {{
    labels: dates,
    datasets: [
      {{ label: '总 IP', data: totalIps, borderColor: '#38bdf8', backgroundColor: 'rgba(56,189,248,.1)', fill: true, tension: .3, pointRadius: 0 }},
      {{ label: '真实活跃用户', data: realUsers, borderColor: '#facc15', backgroundColor: 'rgba(250,204,21,.08)', fill: true, tension: .3, pointRadius: 0 }},
      {{ label: '爬虫/抓取', data: highBots, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,.1)', fill: true, tension: .3, pointRadius: 0 }},
      {{ label: '低活跃', data: lowAct, borderColor: '#64748b', backgroundColor: 'transparent', tension: .3, pointRadius: 0, borderDash: [4,4] }}
    ]
  }},
  options: {{
    responsive: true,
    interaction: {{ intersect: false, mode: 'index' }},
    plugins: {{ legend: {{ labels: {{ color: '#94a3b8', usePointStyle: true }} }} }},
    scales: {{
      x: {{ ticks: {{ color: '#64748b', maxTicksLimit: 15 }} }},
      y: {{ ticks: {{ color: '#64748b' }}, grid: {{ color: '#1e293b' }} }}
    }}
  }}
}});

const tbody = document.querySelector('#table tbody');
for (const d of dates.reverse()) {{
  const s = stats[d];
  const pct = (s.real_active_users / s.total_unique_ips * 100).toFixed(1);
  tbody.innerHTML += `<tr>
    <td>${{d}}</td>
    <td>${{s.total_unique_ips}}</td>
    <td>${{s.real_active_users}}</td>
    <td>${{s.high_req_bots}}</td>
    <td>${{s.low_activity}}</td>
    <td>${{pct}}% <span class="pct">(${{s.real_active_users}}/${{s.total_unique_ips}})</span></td>
  </tr>`;
}}
</script>
</body>
</html>'''
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f"HTML → {out_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Gin 日志每日 IP 统计')
    parser.add_argument('logfile', help='日志文件路径 (支持 .gz)')
    parser.add_argument('--max-items', '-m', type=int, default=200,
                        help='单IP日最多不同内容项数，超出算抓取 (默认 200)')
    parser.add_argument('--mode', choices=('auto', 'comic', 'api'), default='auto',
                        help='auto=自动, comic=漫画站, api=API站')
    parser.add_argument('--output-dir', '-o', default='.', help='输出目录')
    parser.add_argument('--name', '-n', default=None, help='输出文件名前缀')
    parser.add_argument('--no-html', action='store_true', help='只输出 JSON')
    args = parser.parse_args()

    base = args.name or os.path.splitext(os.path.basename(args.logfile))[0]
    base = base.replace('.log', '').replace('.nohup', '').replace('.out', '')
    json_path = os.path.join(args.output_dir, f'{base}_daily_stats.json')
    html_path = os.path.join(args.output_dir, f'{base}_daily_stats.html')

    print(f"解析: {args.logfile}", file=sys.stderr)
    daily = parse_log(args.logfile)

    if args.mode == 'auto':
        has_s = any(
            d['items'] > 0 for date, ips in daily.items()
            for ip, d in list(ips.items())[:50]
        ) if daily else False
        mode = 'comic' if has_s else 'api'
        print(f"检测模式: {mode}", file=sys.stderr)
    else:
        mode = args.mode

    max_items = args.max_items
    print(f"规则: {mode}, 日内容项≤{max_items}, "
          "真人信号: host/proxy参数 + 顺序阅读 + 浏览行为",
          file=sys.stderr)

    stats = compute_stats(daily, max_items, mode)
    for d in sorted(stats):
        s = stats[d]
        pct = s['real_active_users'] * 100 // max(s['total_unique_ips'], 1)
        print(f"  {d}: {s['total_unique_ips']:>5} 总IP, {s['real_active_users']:>5} 真实 ({pct}%), "
              f"{s['high_req_bots']:>4} 抓取, {s['low_activity']:>4} 低活跃")

    with open(json_path, 'w') as fh:
        json.dump(stats, fh, indent=2)
    print(f"JSON → {json_path}", file=sys.stderr)

    if not args.no_html:
        gen_html(stats, f'{base} 每日活跃用户统计', html_path)


if __name__ == '__main__':
    main()
