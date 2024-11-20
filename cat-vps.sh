#!/bin/bash

cat .env | ~/script/ssh.sh -v root@vps.moonchan.xyz 'cat >> .env'