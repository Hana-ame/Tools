#!/bin/bash

if [ $# -eq 0 ]; then
    # No arguments: just connect to the host
    ~/script/ssh/ssh.sh root@vps.moonchan.xyz
else
    # Split arguments: all but the last go before the host, the last goes after
    before=("${@:1:$#-1}")   # all arguments except the last
    last="${@: -1}"          # the last argument
    ~/script/ssh/ssh.sh "${before[@]}" root@vps.moonchan.xyz "$last"
fi