/sbin/ifconfig sit0 down
/sbin/ifconfig sit1 down

/sbin/ifconfig sit0 up
/sbin/ifconfig sit0 inet6 tunnel ::66.220.18.42
/sbin/ifconfig sit1 up
/sbin/ip -6 route add ::/0 dev sit1 metric 2048
/sbin/ip link set dev sit1 mtu 1280

/sbin/ip addr add 2001:470:c:6c::2 dev sit1