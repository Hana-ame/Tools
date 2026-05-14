#!/bin/bash

while true
do
    ssh root@45.130.22.56 "script/kill_process.sh ${1}222"
    ssh root@45.130.22.56 -R ${1}222:127.0.0.1:22 -o ServerAliveInterval=30
done
