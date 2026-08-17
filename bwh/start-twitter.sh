#!/bin/bash
# 一键启动 twitter 服务全家桶 (bwh)
# 参考 cloudcone/vps 的 startup.sh 启动方式:
#   nohup ./twitter.bin & + nohup py caller.py & + nohup py deamon.py &
# bwh 上 twitter.bin 由 systemd (twitter.service) 托管, 这里走 systemctl,
#   避免 nohup 再起一个实例和 systemd 的实例抢 8080 端口 (之前踩过双实例坑)。
# python 两个 server 用 nohup 后台跑, pgrep 做幂等: 重复执行不会起第二份。
# 注意: 不能把 pgrep 模式写成 'start-twitter' 之类会匹配自身命令行/父 shell 的串。

# 1. twitter.bin (内含 twimg 反代, 监听 127.25.9.15:8080 + 主服务 127.25.9.21:8080)
systemctl start twitter

# 2. python 抓取服务
#    caller.py: TCP socket server (127.25.9.19:8080), 收 twitter.bin 转发的 username 调 get2.py
#    deamon.py: 每 15 分钟轮询 commands.txt/pending.txt, 执行抓取指令
cd /root/twitter || exit 1
pgrep -f 'python3 caller.py' >/dev/null || nohup python3 caller.py >> caller.out 2>&1 &
pgrep -f 'python3 deamon.py' >/dev/null || nohup python3 deamon.py >> nohup.out 2>&1 &