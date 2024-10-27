#!/bin/bash

echo -ne "\033]0;反代v.ps:${1}222端口(ssh)\007"


while True
do
	# no need to kill old process
	ssh root@45.130.22.56 -L  ${1}222:127.0.0.1:${1}222 -o ServerAliveInterval=20
done
