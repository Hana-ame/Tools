#!/bin/bash
sudo ip link set dev eth0 mtu 1350

# 等网络真正就绪再往下走。
# 为什么: @reboot 比 network-online.target 更早触发(2026-10-08 实测早 2 秒),
# 网络没通时 git clone / GitHub API 下载必然失败; 又因下面用 && 串联,
# 失败即整条断链, 表现为「服务根本没起」。三个 boot 的对照:
#   10-08 @reboot 16:25:18 vs network 16:25:20
#   10-07 @reboot 16:25:13 vs network 16:25:14
#   10-06 @reboot 16:25:15 vs network 16:25:17
for _i in $(seq 1 60); do
  curl -sf --max-time 5 -o /dev/null https://api.github.com/ && break
  sleep 2
done

# 没写内容。
source ~/script/cloudcone/backup.sh

systemctl start mariadb
systemctl start nginx
systemctl start sshd

# source ~/script/cloudcone/net6.sh

# exhentai
git clone --depth 1 --branch master https://github.com/Hana-ame/api-pack.git temp-repo
rm -rf ~/exhentai
mkdir -p ~/exhentai
cp -r temp-repo/exhentai/main/exhentai/. ~/exhentai/
rm -rf temp-repo

# api-pack
# 下载成功就换新版; 失败也用现有二进制起服务, 不留空窗。
# --pattern 锚定资产名, 防同 release 内其他资产被子串误匹配。
cd ~
if python3 ~/script/download_asset.py --repo Hana-ame/api-pack --dest api-pack-new --pattern myapp-linux-amd64; then
  chmod +x api-pack-new
else
  echo "api-pack 下载失败, 用现有二进制启动: $(date)"
fi
if [ -x api-pack-new ]; then
  nohup ./api-pack-new > ./nohup.out 2>&1 &
else
  echo "api-pack-new 不可执行且下载失败, 无法启动: $(date)"
fi

# azure
# 同上: 下载失败不阻塞, 用现有二进制起。
cd ~;
if [ -f azure/refresh_token ]; then
  cd azure
  if python3 ~/script/download_asset.py --repo Hana-ame/azure-go --dest azure.bin; then
    chmod +x azure.bin
  else
    echo "azure.bin 下载失败, 用现有二进制启动: $(date)"
  fi
  if [ -x azure.bin ]; then
    nohup ./azure.bin > ./nohup.out 2>&1 &
  fi
  cd ~
fi

cd ~/script/ && timeout 120 git pull;

cd /etc/nginx && GIT_MERGE_AUTOEDIT=no timeout 120 git merge -X theirs origin/cloudcone --quiet
