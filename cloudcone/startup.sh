#!/bin/bash

# 没写内容。
source ~/script/cloudcone/backup.sh

systemctl start mariadb
systemctl start nginx
systemctl start sshd

source ~/script/cloudcone/net6.sh

# exhentai
git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo
rm -rf ~/exhentai
mkdir -p ~/exhentai
cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/
rm -rf temp-repo

# api-pack
cd ~;
python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new && chmod +x api-pack-new && nohup ./api-pack-new > ./nohup.out 2>&1 &

# azure
cd ~;
ls azure/refresh_token && cd azure && python3 ~/script/download_asset.py --repo Hana-ame/azure-go --dest azure.bin && chmod +x azure.bin && nohup ./azure.bin > ./nohup.out 2>&1 &

cd ~/script/ && git pull;

cd /etc/nginx && git merge -X theirs origin/cloudcone --quiets