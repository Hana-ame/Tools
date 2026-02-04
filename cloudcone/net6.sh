/sbin/ifconfig sit0 down
/sbin/ifconfig sit1 down

/sbin/ifconfig sit0 up
/sbin/ifconfig sit0 inet6 tunnel ::66.220.18.42
/sbin/ifconfig sit1 up
/sbin/route -A inet6 add ::/0 dev sit1
/sbin/ip link set dev sit1 mtu 1280