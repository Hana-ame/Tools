journalctl --vacuum-time=2d

~/stalker.sh

# v2ray
systemctl start v2ray
iptables -I FORWARD -p tcp --dport 25 -j DROP

# shijima
nohup ./shijima >> nohup.out 2>&1  &

# azure
cd ./azure/
nohup ./azure.bin > nohup.out 2>&1 &


sleep 20;
source ~/script/net6.sh;

cd ~
# w/exhentai
git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo
rm -rf ~/exhentai
mkdir -p ~/exhentai
cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/
rm -rf temp-repo
python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new && chmod +x api-pack-new && nohup ./api-pack-new > ./nohup.out 2>&1 &


cd ~/twitter
python3 ~/script/download_asset.py --repo Hana-ame/twitter-pic-go --dest twitter.bin && chmod +x twitter.bin;
nohup ./twitter.bin >> nohup.out 2>&1  &
nohup py caller.py >> nohup.out 2>&1  &
nohup py deamon.py >> nohup.out 2>&1 &

# azure
cd ~;
ls azure/refresh_token && cd azure && python3 ~/script/download_asset.py --repo Hana-ame/azure-go --dest azure.bin && chmod +x azure.bin && nohup ./azure.bin > ./nohup.out 2>&1 &

sleep 180;

~/backup.sh

cd ~/script && git pull;