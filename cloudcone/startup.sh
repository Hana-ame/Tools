#!/bin/bash

# 没写内容。
source ~/script/cloudcone/backup.sh

systemctl start mariadb
systemctl start nginx
systemctl start sshd

source ~/script/cloudcone/net6.sh

# api-pack
cd ~;
py ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new && nohup ~/api-pack-new > ./nohup.out 2>&1 &

# azure
ls azure/azure.bin && cd azure && py ~/script/download_asset.py --repo Hana-ame/azure --dest azure.bin && nohup ~/azure.bin > ./nohup.out 2>&1 &