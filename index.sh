#!/bin/bash
IFS=$'\n'
# 获取当前目录下的所有子文件夹
dirs=$(find .  -type d)
# 遍历每个子文件夹
for dir in $dirs; do
  # 进入子文件夹
  cd $dir
  # 执行你的命令，比如打印当前路径
  tree -H '.' -L 2 --noreport --dirsfirst -T 'My Site' -s -D --charset utf-8 -I "index.html" -o index.html

  # 返回上一级目录
  cd -
done

