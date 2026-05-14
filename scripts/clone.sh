#!/bin/bash

# https://poe.com/s/J34pt1pzocBYahC0o3Dz

# 检查参数数量
if [ "$#" -lt 2 ]; then
    echo "用法: $0 <仓库URL> <分支名称> [深度]"
    exit 1
fi

# 获取参数
REPO_URL=$1
BRANCH_NAME=$2
DEPTH=$3

# 构建克隆命令
if [ -z "$DEPTH" ]; then
    # 如果没有指定深度
    git clone -b "$BRANCH_NAME" --single-branch "$REPO_URL"
else
    # 如果指定了深度
    git clone -b "$BRANCH_NAME" --single-branch --depth "$DEPTH" "$REPO_URL"
fi

# 检查克隆是否成功
if [ $? -eq 0 ]; then
    echo "成功克隆分支 '$BRANCH_NAME'。"
else
    echo "克隆失败。"
    exit 1
fi