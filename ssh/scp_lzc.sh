#!/bin/bash

# 检查是否提供了文件夹名称参数
if [ $# -ne 1 ]; then
    echo "用法: $0 <文件夹名>"
    echo "示例: $0 livelock_test_1sync"
    exit 1
fi

# 获取文件夹名称（去除末尾可能的斜杠，后续统一添加）
folder_name="${1%/}"

# 检查本地文件夹是否存在
if [ ! -d "$folder_name" ]; then
    echo "错误：文件夹 '$folder_name' 不存在或不是一个目录。"
    exit 1
fi

# 执行SCP命令，注意在源文件夹后添加斜杠以复制内容而非目录本身
scp -r -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa "${folder_name}/" lzc@192.168.1.53:/home/lzc/

# 检查SCP是否成功
if [ $? -eq 0 ]; then
    echo "同步完成：'$folder_name' 已复制到远程主机。"
else
    echo "错误：SCP同步失败。"
    exit 1
fi
