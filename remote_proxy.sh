#!/bin/bash
source ~/script/env.source
while true
do
    (ssh -o "ProxyCommand=nc -X 5 -x $SOCKS_PROXY %h %p" root@bwh.moonchan.xyz -p26275 "~/script/kill_ssh.sh") \
    && \
    (ssh -o "ProxyCommand=nc -X 5 -x $SOCKS_PROXY %h %p" root@bwh.moonchan.xyz -p26275 \
	    -R [2001:470:c:6c::3]:22:localhost:22 \
	    -R [2001:470:c:6c::3]:3000:localhost:3000 \
	    -o ServerAliveInterval=3
    )
    sleep 5
done
