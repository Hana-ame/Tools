# 内网直连, 不走 SOCKS 代理, 故不调 ssh/ssh.sh
# "$@" 引号化: 避免无引号时通配符被本地 glob
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa "$@" lzc@192.168.1.53
