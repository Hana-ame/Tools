#!/bin/bash

cd ~;

# install
apt update && apt upgrade;
apt install nginx;
apt install mariadb;
# acme.sh

# add startup.sh
cd ~;
NEW_JOB="@reboot ~/script/cloudcone/startup.sh";
(crontab -l 2>/dev/null | grep -vF "$NEW_JOB"; echo "$NEW_JOB") | crontab -;

# nginx
cd /etc && rm -rf nginx && git clone git@github.com:Hana-ame/nginx.git -b cloudcone nginx && cd nginx;
cp ~/script/nginx-reload.sh reload.sh;

# 顺手的事
cd ~ && ln -s ~/script/tree.sh;