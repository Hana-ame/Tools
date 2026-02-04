#!/bin/bash

# # 确保~/.ssh目录存在
# mkdir -p ~/.ssh
# chmod 700 ~/.ssh
# # 将GitHub的主机密钥添加到已知主机文件
# ssh-keyscan github.com >> $KNOWN_HOSTS_FILE
# # azure
# mkdir -p ~/azure/ && curl -L https://upload.moonchan.xyz/REPLACE_WITH_FILE_ID/azure_tokens.tar.gz | tar -xz -C ~/azure/
# # rclone
# mkdir -p ~/.config/rclone/ && curl -L https://upload.moonchan.xyz/REPLACE_WITH_FILE_ID/rclone.conf >  ~/.config/rclone/rclone.conf
# curl https://upload.moonchan.xyz/REPLACE_WITH_FILE_ID/.env > .env
# git clone git@github.com:Hana-ame/Tools.git -b script
# ~/script/cloudcone/install.sh


# Stop on any error
set -e

# 0. Load .env file
DOTENV_FILE="$HOME/.env"

if [ -f "$DOTENV_FILE" ]; then
    echo "Loading variables from $DOTENV_FILE..."
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip lines starting with # or empty lines
        [[ $line =~ ^#.* ]] || [[ -z $line ]] && continue
        # Export the variable
        export "$line"
    done < "$DOTENV_FILE"
else
    echo "Error: .env file not found at $DOTENV_FILE"
    exit 1
fi

# install ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCwF4AUmXUJ6eC14jNfe6gTBV3iYvMr6RHuCt356KbuWX/EeVjqNRmTIFam72gfwIUYIJKhekCg4qGwWEetUeFo5Cv2/cGxdd+UfwTSHwEos2jdNFXXlpgLhn/R6c4deuUvXhrfnRI224M9aQZd2SC0Jy1ORC2C1RVp0+u64ZPcHDpbgO/SMVE4JbrEdsTN9wYBqAhAb19TxyPkshsQ5mcDuRWh0a1zi9hmefa7tBHrwAweih3wX+BNij+kBChJrfXQuiw30BGP5XEP4V4bfqiosgqoLJQ4jH7qFQOchABPZ7gR4eHe5/dftv4Y7GUa/gtxzpczYi6YmidwZTaIkv5ZJMNG9wmSOUZLKCSv+qMM5LWLE8VYDVTMN7SMSmBGVqgQnHK6OqOqrPuBvHY+oiKUf8YTb7yX49XLyiGO9K80y3io4IqUTfAAvC0k0N+dKxUCGy0V5BmovwLrrbwq84e+SzUEd1jRliPko4EgiNIcBnuQObbEQa6JsppJL4QasFH/U5tOXGCWkU+cD/mAVykwHe+uKbuc+nvnHkKNh40XSoXVHWwpqWHllp+4o26Kjr8WC0TmoiJ/FmlBgGMSk/P7bLoy8pydQOyt+DIUpBWF85vnKcxkeRZC31EpvmDveZ7V4TOSaGbc0+j9ApWVH2WJGZBRNqzA9rtUOId0T5quDw== luminovoez@gmail.com" >>  ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMdcbLQK62FfDMNo1wjAgw6VlUugmxBrID+ijeHnxRhwMA6Ld/yjQ0Ean338wJoLq7GmfuTlsMocmCVubKNDnG0nyg4M8jkklTZZ76aYp0bAzufqXmkItWMU3uyqWyQDEqJdVKc1OEOY4JGaD+47y7nLWzlsOY0DwBW6BvQrA425fQPhi75KLPn5VBHniikhxoNZdSkywZ+2+4j1eoCpSK+3oRKG3TqdoPONZCjLRJxlgQ9kTgp4BJbBRBSFIv+uXYoNtv/k0B80QK5rIiy6xuns0McQUOfQ/GdyZXt8PNw2YcyqS+u+YkFl32EovPjMP1UB+XjswDvgMtgDep18wN" >>  ~/.ssh/authorized_keys

# 1. 禁用密码验证
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 2. 禁用挑战响应验证（防止备用密码登录方式）
sudo sed -i 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?KbdInteractiveAuthentication.*/KbdInteractiveAuthentication no/' /etc/ssh/sshd_config

cd ~;

# install
apt update -y && apt upgrade -y
apt install socat -y

# acme.sh
curl https://get.acme.sh | sh -s email=luminovoez@gmail.com
alias acme.sh="/root/.acme.sh/acme.sh"
acme.sh --issue --dns dns_cf -d moonchan.xyz -d *.moonchan.xyz
acme.sh --issue --dns dns_cf -d 810114.xyz -d *.810114.xyz
acme.sh --issue --standalone -d moonchan.publicvm.com


# add startup.sh
cd ~;
# Pre-set nano as the selected editor to satisfy the system check
echo 'SELECTED_EDITOR="/usr/bin/nano"' > ~/.selected_editor
NEW_JOB="@reboot sleep 60;~/script/cloudcone/startup.sh";
(crontab -l 2>/dev/null | grep -vF "$NEW_JOB"; echo "$NEW_JOB") | crontab -;

# nginx
apt install nginx -y
cd /etc && rm -rf nginx && git clone https://github.com/Hana-ame/nginx.git -b cloudcone nginx && cd nginx;
ln -s ~/script/nginx-reload.sh reload.sh;

apt install mariadb-server -y

# 顺手的事
cd ~ && ln -s ~/script/tree.sh;

apt install python3 -y
apt install python3-dotenv -y
apt install python3-requests -y

# rclone
curl https://rclone.org/install.sh | bash

# docker
curl -fsSL https://get.docker.com | sh

# 3x-ui
mkdir ~/3x-ui/ -p && cd ~/3x-ui/
cp ~/script/3x-ui.compose.yml compose.yml
docker compose up -d

# azure
mkdir /var/www/upload -p && cd /var/www/upload 
curl https://upload.moonchan.xyz/ > index.html
curl https://upload.moonchan.xyz/sw.js > sw.js
curl https://upload.moonchan.xyz/manifest.json > manifest.json


source ~/script/cloudcone/startup.sh