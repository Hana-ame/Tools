#!/bin/bash

# systemctl start mariadb
systemctl start nginx
systemctl start sshd
# systemctl start v2ray

# source ~/script/bwh/net6.sh

sleep 15;

# twitter-pic: 一键拉起 twitter.bin + python 服务 (caller.py / deamon.py)
bash ~/script/bwh/start-twitter.sh

# # exhentai
# # 1. Shallow clone the master branch into a temporary folder
# git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo

# # 2. Create the target directory if it doesn't exist
# rm -rf ~/exhentai
# mkdir -p ~/exhentai

# # 3. Copy the contents of that specific subfolder to ~/exhentai
# # Note: Using /. at the end copies the contents of the folder, not the folder itself
# cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/

# # 4. Remove the temporary repository
# rm -rf temp-repo

# api-pack
# bwh 上 api-pack 由 systemd 单元托管 (Restart=always, ExecStart=/root/api-pack-new),
# 所以这里必须「停单元 -> 拉新版 -> 起单元」, 不能像 cloudcone 那样 nohup 直起,
# 否则会起第二个实例抢占端口。
cd ~;
systemctl stop api-pack;
if python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new --pattern myapp-linux-amd64; then
  chmod +x api-pack-new && systemctl start api-pack;
else
  echo "api-pack 下载失败, 用现有二进制重启" && systemctl start api-pack;
fi

# nohup /usr/local/bin/py ~/forward.py &
# nohup /usr/local/bin/py ~/forward.py --local-port 22  --remote-port 26275 &

cd ~/script/ && git pull;
