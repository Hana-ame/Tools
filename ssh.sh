ssh \
	  -o "ProxyCommand=nc -X5 -x $SOCKS_PROXY %h %p" \
	    -o ServerAliveInterval=5 \
	      -o ServerAliveCountMax=14 \
	        -o TCPKeepAlive=yes \
		  -o IPQoS=throughput \
		    $@

