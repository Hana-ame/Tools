#!/bin/bash

# ================= 配置区域 =================
# 1. HE.net 的隧道服务器 IP (Server IPv4 Address)
#    (也就是你原来脚本里 route add ::66... 的那个地址)
REMOTE_IP="216.66.80.30" 

# 2. 本机 IPv4 地址 (你的 eth0 上的 IPv4)
#    (根据你的 ifconfig，填你 eth0 的 IP 45.130.22.56)
LOCAL_IP="45.130.22.56"

# 3. 你的 HE.net IPv6 地址 (Client IPv6 Address)
#    (这是你 sit1 上的 IP)
IPV6_ADDR="2001:470:1f0a:6b1::2/64"

# 4. 你的 IPv6 网段 (去掉最后的 ::2/64，改成 ::/64)
#    (用于策略路由规则匹配)
IPV6_SUBNET="2001:470:1f0a:6b1::/64"
# ===========================================

# --- 1. 清理环境 (防止脚本重复运行报错) ---
ip link set sit1 down 2>/dev/null
ip tunnel del sit1 2>/dev/null
# 删除旧的策略路由规则，防止重复堆叠
ip -6 rule del from $IPV6_SUBNET table 200 2>/dev/null

# --- 2. 创建隧道接口 ---
# 使用现代 iproute2 命令，替代过时的 ifconfig
ip tunnel add sit1 mode sit remote $REMOTE_IP local $LOCAL_IP ttl 255
ip link set sit1 up

# --- 3. 绑定 IPv6 地址 ---
ip addr add $IPV6_ADDR dev sit1
# 如果有多个 IP，可以在这里继续加：
# ip addr add 2001:470:1f0a:6b1::3/64 dev sit1

# --- 4. 配置策略路由 (关键步骤！) ---
# 解释：不修改主路由表，而是新建一个表(200)给隧道用

# A. 在表 200 中添加默认路由指向 sit1
ip -6 route add default dev sit1 table 200

# B. 添加规则：凡是源 IP 属于 HE 网段的包，去查表 200
ip -6 rule add from $IPV6_SUBNET lookup 200

echo "IPv6 Tunnel Configured with Policy Routing."