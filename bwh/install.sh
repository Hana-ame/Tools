#!/bin/bash

# curl -fsSL https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/script/bwh/install.sh | bash

# 这一段是让你在console里面运行的。
apt update -y && apt upgrade -y
apt install git -y
apt install curl -y
apt install sudo -y
# # 确保~/.ssh目录存在
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# # 将GitHub的主机密钥添加到已知主机文件
# ssh-keyscan github.com >>  ~/.ssh/known_hosts 
cd ~ && git clone https://github.com/Hana-ame/Tools.git -b script script
# git clone git@github.com:Hana-ame/Tools.git -b script script
# ~/script/bwh/install.sh

# Stop on any error
set -e


# install ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCwF4AUmXUJ6eC14jNfe6gTBV3iYvMr6RHuCt356KbuWX/EeVjqNRmTIFam72gfwIUYIJKhekCg4qGwWEetUeFo5Cv2/cGxdd+UfwTSHwEos2jdNFXXlpgLhn/R6c4deuUvXhrfnRI224M9aQZd2SC0Jy1ORC2C1RVp0+u64ZPcHDpbgO/SMVE4JbrEdsTN9wYBqAhAb19TxyPkshsQ5mcDuRWh0a1zi9hmefa7tBHrwAweih3wX+BNij+kBChJrfXQuiw30BGP5XEP4V4bfqiosgqoLJQ4jH7qFQOchABPZ7gR4eHe5/dftv4Y7GUa/gtxzpczYi6YmidwZTaIkv5ZJMNG9wmSOUZLKCSv+qMM5LWLE8VYDVTMN7SMSmBGVqgQnHK6OqOqrPuBvHY+oiKUf8YTb7yX49XLyiGO9K80y3io4IqUTfAAvC0k0N+dKxUCGy0V5BmovwLrrbwq84e+SzUEd1jRliPko4EgiNIcBnuQObbEQa6JsppJL4QasFH/U5tOXGCWkU+cD/mAVykwHe+uKbuc+nvnHkKNh40XSoXVHWwpqWHllp+4o26Kjr8WC0TmoiJ/FmlBgGMSk/P7bLoy8pydQOyt+DIUpBWF85vnKcxkeRZC31EpvmDveZ7V4TOSaGbc0+j9ApWVH2WJGZBRNqzA9rtUOId0T5quDw== luminovoez@gmail.com" >>  ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMdcbLQK62FfDMNo1wjAgw6VlUugmxBrID+ijeHnxRhwMA6Ld/yjQ0Ean338wJoLq7GmfuTlsMocmCVubKNDnG0nyg4M8jkklTZZ76aYp0bAzufqXmkItWMU3uyqWyQDEqJdVKc1OEOY4JGaD+47y7nLWzlsOY0DwBW6BvQrA425fQPhi75KLPn5VBHniikhxoNZdSkywZ+2+4j1eoCpSK+3oRKG3TqdoPONZCjLRJxlgQ9kTgp4BJbBRBSFIv+uXYoNtv/k0B80QK5rIiy6xuns0McQUOfQ/GdyZXt8PNw2YcyqS+u+YkFl32EovPjMP1UB+XjswDvgMtgDep18wN" >>  ~/.ssh/authorized_keys

# 1. 禁用密码验证
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 2. 禁用挑战响应验证（防止备用密码登录方式）
sed -i 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?KbdInteractiveAuthentication.*/KbdInteractiveAuthentication no/' /etc/ssh/sshd_config

cd ~;


# add startup.sh
cd ~;
# Pre-set nano as the selected editor to satisfy the system check
echo 'SELECTED_EDITOR="/usr/bin/nano"' > ~/.selected_editor
NEW_JOB="@reboot sleep 60;~/script/bwh/startup.sh";
(crontab -l 2>/dev/null | grep -vF "$NEW_JOB"; echo "$NEW_JOB") | crontab -;


# 关闭交换文件
sudo swapoff /swap

# 删除原文件
sudo rm /swap

# 重新创建新大小的文件（步骤同上）
sudo fallocate -l 2G /swap
sudo chmod 600 /swap
sudo mkswap /swap
sudo swapon /swap


# acme.sh
curl https://get.acme.sh | sh -s email=luminovoez@gmail.com
alias acme.sh="/root/.acme.sh/acme.sh"
acme.sh --issue --standalone -d bwh.moonchan.xyz --keylength ec-256


apt install nginx -y
cd /etc && rm -rf nginx && git clone  https://github.com/Hana-ame/nginx.git -b bwh