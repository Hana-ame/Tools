#!/bin/bash

systemctl start mariadb
systemctl start nginx
systemctl start sshd
systemctl start v2ray

source ~/script/net6.sh

sleep 15;
py  ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new
nohup /root/api-pack-new &

nohup /usr/local/bin/py ~/forward.py &
nohup /usr/local/bin/py ~/forward.py --local-port 22  --remote-port 26275 &