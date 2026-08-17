#!/bin/bash

cat .env | ~/script/ssh/ssh.sh -p26275 root@bwh.moonchan.xyz 'cat >> .env'