#!/bin/bash

while true
do
    ssh root@bwh.moonchan.xyz -p26275 "~/script/kill_ssh.sh"
    ssh root@bwh.moonchan.xyz -p26275 \
	    -R [2001:470:c:6c::3]:22:localhost:22 \
	    -R [2001:470:c:6c::3]:3000:localhost:3000 \
	    -o ServerAliveInterval=30
done
