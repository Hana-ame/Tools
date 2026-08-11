#!/bin/bash

if [ $# -eq 0 ]; then
    # No arguments: just connect to the host
    ~/script/ssh/ssh.sh root@bwh.moonchan.xyz -p26275
else
    # Split arguments: all but the last go before the host, the last goes after
    before=("${@:1:$#-1}")   # all arguments except the last
    last="${@: -1}"          # the last argument
    ~/script/ssh/ssh.sh -p26275 "${before[@]}" root@bwh.moonchan.xyz "$last"
fi
