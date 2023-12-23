#!/bin/bash

while True
do
	ssh root@45.130.22.56 -L  1935:a.rtmp.youtube.com:1935 -o ServerAliveInterval=20

done
