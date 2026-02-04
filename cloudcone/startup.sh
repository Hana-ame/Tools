#!/bin/bash

# 没写内容。
source ~/script/cloudcone/backup.sh

systemctl start mariadb
systemctl start nginx
systemctl start sshd

source ~/script/cloudcone/net6.sh

# api-pack
cd ~;
python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new && nohup ~/api-pack-new > ./nohup.out 2>&1 &

# azure
cd ~;
ls azure/refresh_token && cd azure && python3 ~/script/download_asset.py --repo Hana-ame/azure-go --dest azure.bin && nohup ~/azure.bin > ./nohup.out 2>&1 &