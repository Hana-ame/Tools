#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 'cookie_string'"
    exit 1
fi

# Escape single quotes in the cookie for safe shell passing
COOKIE="${1//\'/\'\\\'\'}"

for script in ~/script/ssh/bwh.sh ~/script/ssh/vps.sh ~/script/ssh/cloudcone.sh; do
    # 关键修改：在 \$ENV{COOKIE} 两侧添加 \" 双引号
    $script "COOKIE='$COOKIE' perl -i -pe 's/^#next_cookie$/EXHENTAI_PROXY_COOKIE=\"\$ENV{COOKIE}\"\n#next_cookie/' ~/.env"
done