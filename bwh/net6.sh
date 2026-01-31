sleep 10;

/sbin/ifconfig sit0 down
/sbin/ifconfig sit1 down

/sbin/ifconfig sit0 up
/sbin/ifconfig sit0 inet6 tunnel ::45.32.66.87
/sbin/ifconfig sit1 up
/sbin/route -A inet6 add ::/0 dev sit1