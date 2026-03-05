ssh \
	-o "ProxyCommand=nc -X5 -x $SOCKS_PROXY %h %p" \
	-o ServerAliveInterval=1 \
	-o ServerAliveCountMax=124 \
	-o TCPKeepAlive=yes \
	-o IPQoS=throughput \
	$@

