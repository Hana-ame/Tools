#!/bin/bash
# scp 到 cloudcone（走 SOCKS 代理，与 ssh.sh 一致）
# 用法: scp_cloudcone.sh <本地文件/目录> <远程路径>
# 示例: scp_cloudcone.sh chatto.toml /opt/chatto/

if [ $# -ne 2 ]; then
    echo "用法: $0 <本地路径> <远程路径>"
    exit 1
fi

src="$1"
dst="$2"

# 与 ssh.sh 相同的代理配置
PROXY_CMD="nc -X5 -x ${SOCKS_PROXY:-172.29.80.1:10808} %h %p"

scp \
    -o "ProxyCommand=$PROXY_CMD" \
    -o ServerAliveInterval=1 \
    -o ServerAliveCountMax=124 \
    -o TCPKeepAlive=yes \
    -r "$src" "root@cloudcone.moonchan.xyz:$dst"

if [ $? -eq 0 ]; then
    echo "传输完成: $src -> cloudcone:$dst"
else
    echo "错误: scp 失败"
    exit 1
fi
