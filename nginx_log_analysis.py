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
            # Nginx 日志通常是由空格分隔的
            parts = line.split()
            
            # 确保至少有两列数据
            if len(parts) >= 2:
                ip1 = parts[0]
                ip2 = parts[1]
                
                # 核心逻辑：
                # 统计 key = 第二个 ip
                # 如果第二个 ip 为 "-"，时，key = 第一个 ip
                target_ip = ip2
                if target_ip == '-':
                    target_ip = ip1
                
                # 只有当解析出的 IP 有效时才统计 (排除完全是空的情况)
                if target_ip and target_ip != '-':
                    ip_counts[target_ip] += 1
                    total_hits += 1
                    
        except Exception:
            # 遇到格式极度错误的行跳过
            continue

    if not ip_counts:
        print("无有效数据")
        return

    # 2. 准备数据
    sorted_data = ip_counts.most_common()
    # 动态计算 IP 列宽 (为了美观，至少给 15 字符)
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

        # 格式化输出
        print(f"{rank:>3}. {ip:<{max_ip_len}} : {count:>5}   {percentage:>7.2f}%   {cum_percentage:>7.2f}%")

if __name__ == "__main__":
    main()
