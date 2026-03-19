/sbin/ifconfig sit0 down
/sbin/ifconfig sit1 down

/sbin/ifconfig sit0 up
/sbin/ifconfig sit0 inet6 tunnel ::66.220.18.42
/sbin/ifconfig sit1 up
/sbin/ip -6 route add ::/0 dev sit1 metric 2048
/sbin/ip link set dev sit1 mtu 1280

/sbin/ip addr add 2001:470:c:6c::2 dev sit1
# /sbin/ip addr change 2001:470:c:6c::2/128 dev sit1 preferred_lft forever

# /sbin/ip addr del 2607:f130:0:159::9b8b:826f/64 dev eth0
# /sbin/ip addr del 2607:f130:0:159::483d:96da/64 dev eth0
# /sbin/ip addr del 2607:f130:0:159::151d:8350/64 dev eth0