# 经 SOCKS 代理 scp 到 vps; "$@" 引号化避免通配符被本地 glob
scp -o "ProxyCommand=nc -X5 -x $SOCKS_PROXY %h %p" -o ServerAliveInterval=30 "$@"
