#!/bin/bash

echo -ne "\033]0;反代v.ps:1935端口(rmtp)\007"

while true
do
	ssh root@45.130.22.56 -L  1935:a.rtmp.youtube.com:1935 -o ServerAliveInterval=20
done
