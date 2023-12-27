#!/bin/bash
# usage: bash nc_proxy.sh [dest_port] [listen_port] ["6"|"4"|""]

while true
do
  nc -$3lp $2 -c "nc 127.0.0.1 $1"
done
