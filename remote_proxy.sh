#!/bin/bash
source ~/script/env.source
while true
do
    # (ssh -vN -o "ProxyCommand=nc -X 5 -x $SOCKS_PROXY %h %p" root@bwh.moonchan.xyz -p 26275  "~/script/kill_ssh.sh"); \
    (ssh -vN -o "ProxyCommand=nc -X 5 -x $SOCKS_PROXY %h %p" root@bwh.moonchan.xyz -p 26275 \
	    -R [2001:470:c:6c::3]:22:localhost:22 \
	    -R [2001:470:c:6c::3]:3000:localhost:3000 \
	    -R [2001:470:c:6c::3]:443:localhost:443 \
	    -R [2001:470:c:6c::3]:80:localhost:80 \
	    -R [2001:470:c:6c::3]:3389:DESKTOP-LLULJ2Q:3389 \
	    -o ServerAliveInterval=2 -o "ExitOnForwardFailure yes"
    );
    sleep 55;
done
