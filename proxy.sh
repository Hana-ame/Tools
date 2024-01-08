#!/bin/bash

while True
do
    ssh root@45.130.22.56 "script/kill_process.sh 9222"
    ssh root@45.130.22.56 -R 9222:127.0.0.1:22 -o ServerAliveInterval=30
done
