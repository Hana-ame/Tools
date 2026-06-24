#!/bin/bash

# 1. 强制加载系统环境变量，确保 sh 能认识 py 命令
source /etc/profile
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

# 2. 将波浪号 ~ 全部替换为绝对路径 /root，防止 crontab 解析失败
BASE_DIR="/root"

# 任务一：组合命令并通过管道传给 py
( 
  cat ${BASE_DIR}/nohup.out | grep coo | grep -v 127.0.0.1
  printf '\n\n\n'
  cat ${BASE_DIR}/nohup.out | grep bid=23 | grep -v 127.0.0.1
  printf '\n\n\n'
  cat ${BASE_DIR}/nohup.out | grep bid=101 | grep -v 127.0.0.1
  printf '\n\n\n'
  cat ${BASE_DIR}/nohup.out | grep 99999
) | /usr/bin/py ${BASE_DIR}/upload.py --gzip


# 任务二：直接读取文件传给 py
/usr/bin/py ${BASE_DIR}/upload.py ${BASE_DIR}/twitter/nohup.out --gzip

/sbin/reboot;
