import sys
from collections import Counter

def main():
    ip_counts = Counter()
    total_hits = 0

    # 1. 读取并统计
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            parts = line.split('|')
            if len(parts) >= 4:
                ip = parts[3].strip()
                if ip:
                    ip_counts[ip] += 1
                    total_hits += 1
        except Exception:
            continue

    if not ip_counts:
        print("无有效数据")
        return

    # 2. 准备数据
    sorted_data = ip_counts.most_common()
    # 动态计算 IP 列宽
    max_ip_len = max((len(ip) for ip, _ in sorted_data), default=15)

    # 3. 输出结果
    print(f"Total Hits: {total_hits}")
    # 动态调整分割线长度
    print("-" * (max_ip_len + 40)) 
    
    # 表头
    print(f"{'No.':>3}  {'IP Address':<{max_ip_len}}   {'Count':>5}   {'Percent':>8}   {'Cumul.%':>8}")

    cumulative_count = 0
    for rank, (ip, count) in enumerate(sorted_data, 1):
        # 计算百分比
        percentage = (count / total_hits) * 100
        cumulative_count += count
        cum_percentage = (cumulative_count / total_hits) * 100

        # 格式化输出 (去掉括号，使用空格分隔)
        print(f"{rank:>3}. {ip:<{max_ip_len}} : {count:>5}   {percentage:>7.2f}%   {cum_percentage:>7.2f}%")

if __name__ == "__main__":
    main()
