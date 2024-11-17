#!/bin/bash

# 记录原来的branch
current_commit_hash=$(git rev-parse HEAD)

echo "$current_commit_hash"

git checkout master
master_commit_hash=$(git rev-parse HEAD)

git reset --hard "$current_commit_hash"
git push -f
git reset --hard "$master_commit_hash"

git cherry-pick "$current_commit_hash"

echo "按下 Enter 键继续..."
read

git commit
git push -f

# 切回原来的branch
git checkout "$current_commit_hash"