#!/bin/bash

# 1. 获取当前 commit 的短哈希值 (前 7 位)
# 如果你需要完整的哈希值，请将 --short 去掉
COMMIT_HASH=$(git rev-parse --short HEAD)

# 2. 构造 Tag 名称
TAG_NAME="v0.0.0-$COMMIT_HASH"

echo "目标 Tag: $TAG_NAME"

# 3. 在本地创建 Tag
if git tag "$TAG_NAME"; then
    echo "成功在本地创建 Tag: $TAG_NAME"
else
    echo "错误: 创建 Tag 失败，可能该 Tag 已存在。"
    exit 1
fi

# 4. 推送 Tag 到远程 origin
echo "正在推送 Tag 到 origin..."
if git push origin "$TAG_NAME"; then
    echo "推送成功！GitHub Action 应该已经开始触发。"
else
    echo "错误: 推送 Tag 失败。"
    # 如果推送失败，通常建议也删除本地标签以便下次重试
    git tag -d "$TAG_NAME"
    exit 1
fi

# 5. 在本地删除该 Tag
echo "正在删除本地 Tag 以保持环境整洁..."
if git tag -d "$TAG_NAME"; then
    echo "本地 Tag 已删除。"
else
    echo "警告: 本地 Tag 删除失败。"
fi

echo "所有操作已完成。"
