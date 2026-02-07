/sbin/ifconfig sit0 down;
/sbin/ifconfig sit1 down;

/sbin/ifconfig sit0 up;
/sbin/ifconfig sit0 inet6 tunnel ::216.66.80.30;
/sbin/ifconfig sit1 up;

# 请将下面的 CIDR 换成你 sit1 对应的网段，或者是具体的 IP
/sbin/ip -6 rule add from 2001:470:1f0a:6b1::/64 lookup 100

/sbin/ip -6 route add default dev sit1 table 100
/sbin/ip link set mtu 1280 dev sit1