ssh -o "ProxyCommand=nc -X5 -x $SOCKS_PROXY %h %p" -o ServerAliveInterval=30 $@
