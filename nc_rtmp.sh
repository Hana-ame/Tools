#!/bin/bash
# usage: bash nc_proxy.sh [dest_port] [listen_port] ["6"|"4"|""]

while true
do
  ncat -$1vlp 1935 -c "ncat a.rtmp.youtube.com 1935"
  sleep 30
done
