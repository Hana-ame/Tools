#!/bin/bash

systemctl start mariadb
systemctl start nginx
systemctl start sshd
systemctl start v2ray

source ~/script/net6.sh

sleep 15;


# exhentai
# 1. Shallow clone the master branch into a temporary folder
git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo

# 2. Create the target directory if it doesn't exist
rm -rf ~/exhentai
mkdir -p ~/exhentai

# 3. Copy the contents of that specific subfolder to ~/exhentai
# Note: Using /. at the end copies the contents of the folder, not the folder itself
cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/

# 4. Remove the temporary repository
rm -rf temp-repo

# api-pack
cd ~;
python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new && chmod +x api-pack-new && nohup ./api-pack-new > ./nohup.out 2>&1 &

nohup /usr/local/bin/py ~/forward.py &
nohup /usr/local/bin/py ~/forward.py --local-port 22  --remote-port 26275 &

cd ~/script/ && git pull;