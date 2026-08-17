#!/bin/bash

# 统一走 ssh/ssh.sh (修复版: "$@" 引号化, 避免 * 被本地 glob)
~/script/ssh/ssh.sh -4 root@vps.moonchan.xyz "$@"
