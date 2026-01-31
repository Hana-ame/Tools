#!/bin/bash
# 并发curl脚本，统计成功和失败数量

# 检查参数
if [ -z "$1" ]; then
  echo "错误：请提供URL作为第一个参数"
  echo "用法: $0 <URL> [并发数] [超时时间]"
  echo "示例: $0 https://example.com 10 5"
  exit 1
fi

URL="$1"
CONCURRENCY="${2:-10}"  # 第二个参数为并发数，默认为10
TIMEOUT="${3:-10}"      # 第三个参数为超时时间，默认为10秒

# 统计变量
SUCCESS_COUNT=0
FAIL_COUNT=0

echo "开始并发请求..."
echo "目标URL: $URL"
echo "并发数: $CONCURRENCY"
echo "超时时间: ${TIMEOUT}秒"
echo "=========="

# 记录开始时间
start_time=$(date +%s.%N)

# 使用函数处理每个请求
make_request() {
  local req_num=$1
  curl -s -o /dev/null -w "%{http_code}" -m $TIMEOUT "$URL" 2>/dev/null
  local exit_code=$?
  
  if [ $exit_code -eq 0 ]; then
    # HTTP状态码在200-299之间视为成功
    local status_code="$REPLY"
    if [[ $status_code =~ ^2[0-9]{2}$ ]]; then
      echo "请求 #$req_num: 成功 (HTTP $status_code)"
      return 0
    else
      echo "请求 #$req_num: 失败 (HTTP $status_code)"
      return 1
    fi
  else
    echo "请求 #$req_num: 失败 (curl错误码: $exit_code)"
    return 1
  fi
}

# 启动并发请求并收集结果
pids=()
for i in $(seq 1 $CONCURRENCY); do
  make_request $i &
  pids[$i]=$!
done

# 等待所有进程完成并统计结果
for i in $(seq 1 $CONCURRENCY); do
  wait ${pids[$i]}
  exit_status=$?
  if [ $exit_status -eq 0 ]; then
    ((SUCCESS_COUNT++))
  else
    ((FAIL_COUNT++))
  fi
done

# 计算总耗时
end_time=$(date +%s.%N)
total_time=$(echo "$end_time - $start_time" | bc)

echo "=========="
echo "统计结果:"
echo "成功: $SUCCESS_COUNT 个"
echo "失败: $FAIL_COUNT 个"
printf "总耗时: %.2f 秒\n" $total_time
echo "成功率: $(echo "scale=2; $SUCCESS_COUNT * 100 / $CONCURRENCY" | bc)%"
