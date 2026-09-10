journalctl --vacuum-time=2d

# 全脚本日志: 半夜自启动失败的原因,以后有日志可查,不用再猜
exec >> /root/startup.log 2>&1
echo "=== startup.sh start: $(date) ==="

~/stalker.sh

# v2ray
systemctl start v2ray
iptables -I FORWARD -p tcp --dport 25 -j DROP

# shijima
nohup ./shijima >> nohup.out 2>&1  &

# azure
cd ./azure/
nohup ./azure.bin > nohup.out 2>&1 &

sleep 10;
source ~/script/vps/net6.sh;

cd ~
# w/exhentai
git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo
rm -rf ~/exhentai
mkdir -p ~/exhentai
cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/
rm -rf temp-repo
# api-pack: 下载失败/超时不能阻塞启动,回退到现有二进制;下载到 .tmp 再原子换入,避免半截文件
# (坑: 之前 download_asset.py 一次瞬时失败导致 && 断链,整个 api-pack 没起来,且 cron 无日志)
timeout 180 python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new.tmp && mv -f api-pack-new.tmp api-pack-new && chmod +x api-pack-new
nohup ./api-pack-new > ./nohup.out 2>&1 &

# twitter-pic: 注意 asset 要选 twitter-linux-amd64, 默认 pattern(linux-amd64) 会误下 gallery
cd ~/twitter
python3 ~/script/download_asset.py --repo Hana-ame/twitter-pic-go --pattern twitter-linux-amd64 --dest twitter.bin && chmod +x twitter.bin;
nohup ./twitter.bin --addr=127.25.9.21:8080 > nohup.out 2>&1  &
nohup py caller.py > nohup.out 2>&1  &
nohup py deamon.py > nohup.out 2>&1 &

# azure
cd ~;
ls azure/refresh_token && cd azure && python3 ~/script/download_asset.py --repo Hana-ame/azure-go --dest azure.bin && chmod +x azure.bin && nohup ./azure.bin > ./nohup.out 2>&1 &

sleep 180;

~/script/vps/backup.sh

cd ~/script && git pull;