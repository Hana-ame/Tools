#!/usr/bin/env python3
"""zen-multi 分时段统计: 只统计 POST /chat/completions 的成功率。

请求 = '-> POST /chat/completions' 行; 成功 = ': done' 行。
按日志顺序配对(每请求至多一个成功), 成功率 = 配对成功数 / 请求数。

数据源: journalctl -u zen-multi.service 或已保存的日志文件。
用法:
    python3 zen_log_stats.py                 # 今日全部, 按小时
    python3 zen_log_stats.py --since 15:00   # 今日 15:00 起
    python3 zen_log_stats.py --since "2026-08-03 15:00" --until "2026-08-03 17:00"
    python3 zen_log_stats.py --file /tmp/zm_today.log
    python3 zen_log_stats.py --bucket 10m    # 按10分钟分桶
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, deque

TS_RE = re.compile(r"\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.\d+\]")
COMPLETION_RE = re.compile(r"-> POST /chat/completions")
MODELS_RE = re.compile(r"GET /v1/models")
DONE_SRC_RE = re.compile(r"(\w+): done ")


def load_lines(file_path=None, since=None, until=None):
    if file_path:
        with open(file_path, encoding="utf-8", errors="replace") as fh:
            return fh.readlines()
    cmd = ["journalctl", "-u", "zen-multi.service", "--no-pager"]
    if since:
        cmd += ["--since", since]
    if until:
        cmd += ["--until", until]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"读取日志失败: {exc}", file=sys.stderr)
        sys.exit(1)


def parse(lines):
    """按行数 SUCCESS / FAIL 单词统计。
    req: 每个 '-> POST /chat/completions' 的 ts
    ok/fail: 每行 'SUCCESS' / 'FAIL' 的 ts
    """
    reqs, oks, fails, src_done, n_models = [], [], [], Counter(), 0
    for ln in lines:
        mt = TS_RE.search(ln)
        if not mt:
            continue
        ts = mt.group(1)
        if COMPLETION_RE.search(ln):
            reqs.append(ts)
            continue
        if MODELS_RE.search(ln):
            n_models += 1
            continue
        if " SUCCESS" in ln:
            oks.append(ts)
            continue
        if " FAIL" in ln:
            fails.append(ts)
            continue
        ms = DONE_SRC_RE.search(ln)
        if ms:
            src_done[ms.group(1)] += 1
    return reqs, oks, fails, src_done, n_models
    return reqs, oks, fails, src_done, n_models


def fmt_bucket(ts, bucket_min):
    if bucket_min >= 60:
        h = int(ts[11:13]) // (bucket_min // 60) * (bucket_min // 60)
        return f"{ts[0:10]} {h:02d}时"
    return ts[11:16]


def main():
    ap = argparse.ArgumentParser(description="zen-multi completion 请求分时段统计")
    ap.add_argument("--since", help="起始时间 (如 15:00 或 2026-08-03 15:00)")
    ap.add_argument("--until", help="结束时间")
    ap.add_argument("--file", help="从日志文件读取 (否则走 journalctl)")
    ap.add_argument("--bucket", default="60m", help="分桶粒度: 60m/30m/10m/1h (默认 60m)")
    args = ap.parse_args()

    bucket_min = {"60m": 60, "30m": 30, "10m": 10, "1h": 60}.get(args.bucket)
    if not bucket_min:
        print(f"无效 bucket: {args.bucket}", file=sys.stderr)
        sys.exit(1)

    reqs, oks, fails, src_done, n_models = parse(load_lines(args.file, args.since, args.until))

    if not reqs:
        print("时间段内无 completion 请求")
        return

    bucket_req = Counter(fmt_bucket(ts, bucket_min) for ts in reqs)
    bucket_ok = Counter(fmt_bucket(ts, bucket_min) for ts in oks)
    bucket_fail = Counter(fmt_bucket(ts, bucket_min) for ts in fails)

    buckets = sorted(set(bucket_req) | set(bucket_ok) | set(bucket_fail))
    print(f"{'时段':<14} {'请求':>5} {'成功':>5} {'失败':>5} {'成功率':>7}")
    print("-" * 42)
    for b in buckets:
        r, d = bucket_req[b], bucket_ok[b]
        rate = f"{d / r * 100:.0f}%" if r else "-"
        print(f"{b:<14} {r:>5} {d:>5} {bucket_fail[b]:>5} {rate:>7}")
    print("-" * 42)
    total_rate = f"{len(oks) / len(reqs) * 100:.0f}%"
    print(f"合计: 请求 {len(reqs)}  成功 {len(oks)}  成功率 {total_rate}"
          f"{f'  (models 请求 {n_models} 未统计)' if n_models else ''}")
    if src_done:
        print(f"按源: {', '.join(f'{k}={v}' for k, v in sorted(src_done.items()))}")


if __name__ == "__main__":
    main()
