#!/usr/bin/env bash
# hostswitch.sh - 用 nslookup 解析域名,一键切换 /etc/hosts 中的 IPv4/IPv6 记录
# 用法: ./hostswitch.sh <域名> [ipv4|ipv6|auto]
#   auto : 默认模式,交互式选择
#   带参 : 直接切换,无需交互

set -euo pipefail

HOSTS_FILE="/etc/hosts"
DOMAIN="${1:-}"
MODE="${2:-auto}"

usage() {
  echo "用法: $0 <域名> [ipv4|ipv6]"
  echo "  用 nslookup 解析域名,并切换 /etc/hosts 中的 IPv4/IPv6 记录"
  echo "  例: $0 example.com        # 交互选择"
  echo "      $0 example.com ipv6   # 直接切到 IPv6"
  exit 1
}

[ -z "$DOMAIN" ] && usage

# --- 用 host/nslookup 解析 A(IPv4) 和 AAAA(IPv6) ---
if command -v host >/dev/null 2>&1; then
  ipv4_list=$(host -t A "$DOMAIN" 2>/dev/null | awk '/has address/{print $NF}' || true)
  ipv6_list=$(host -t AAAA "$DOMAIN" 2>/dev/null | awk '/has IPv6 address/{print $NF}' || true)
else
  ipv4_list=$(nslookup -type=A "$DOMAIN" 2>/dev/null | awk '/has address/{print $NF}' || true)
  ipv6_list=$(nslookup -type=AAAA "$DOMAIN" 2>/dev/null | awk '/has AAAA address/{print $NF}' || true)
fi

mapfile -t IPV4 <<<"$ipv4_list"
mapfile -t IPV6 <<<"$ipv6_list"

echo "== $DOMAIN 解析结果 =="
echo "IPv4: ${IPV4[*]:-无}"
echo "IPv6: ${IPV6[*]:-无}"

pick() {
  local arr=("$@")
  [ ${#arr[@]} -eq 0 ] && return 1
  [ ${#arr[@]} -eq 1 ] && { echo "${arr[0]}"; return 0; }
  local i n
  for i in "${!arr[@]}"; do echo "$((i+1))) ${arr[$i]}"; done
  read -rp "选择地址编号: " n
  echo "${arr[$((n-1))]}"
}

case "$MODE" in
  ipv4)
    [ ${#IPV4[@]} -eq 0 ] && { echo "没有 IPv4 记录"; exit 1; }
    TARGET=$(pick "${IPV4[@]}") ;;
  ipv6)
    [ ${#IPV6[@]} -eq 0 ] && { echo "没有 IPv6 记录"; exit 1; }
    TARGET=$(pick "${IPV6[@]}") ;;
  auto)
    if [ ${#IPV6[@]} -gt 0 ]; then
      echo ""
      echo "当前解析到 IPv6 地址,选择切换目标:"
      echo "1) IPv4 ($(echo "${IPV4[*]:-无}"))"
      echo "2) IPv6 ($(echo "${IPV6[*]:-无}"))"
      read -rp "选择 (1/2): " ans
      case "$ans" in
        1) [ ${#IPV4[@]} -eq 0 ] && { echo "没有 IPv4 记录"; exit 1; }
           TARGET=$(pick "${IPV4[@]}") ;;
        2) TARGET=$(pick "${IPV6[@]}") ;;
        *) echo "无效选择"; exit 1 ;;
      esac
    elif [ ${#IPV4[@]} -gt 0 ]; then
      TARGET=$(pick "${IPV4[@]}")
      echo "提示: 该域名没有 IPv6 记录,只能切换 IPv4"
    else
      echo "错误: nslookup 解析不到任何地址"; exit 1
    fi ;;
esac

# --- 修改 /etc/hosts ---
[ -w "$HOSTS_FILE" ] || { echo "需要 root 权限,请用 sudo 运行"; exit 1; }

grep -v -E "[[:space:]]$DOMAIN([[:space:]]|$)" "$HOSTS_FILE" > "$HOSTS_FILE.tmp"
printf '%-40s %s\n' "$TARGET" "$DOMAIN" >> "$HOSTS_FILE.tmp"
mv "$HOSTS_FILE.tmp" "$HOSTS_FILE"

echo "== 已写入 /etc/hosts: $TARGET $DOMAIN =="

# --- 刷新 DNS 缓存(尽力而为) ---
command -v resolvectl >/dev/null && resolvectl flush-caches 2>/dev/null || true
command -v systemd-resolve >/dev/null && systemd-resolve --flush-caches 2>/dev/null || true
command -v nscd >/dev/null && systemctl restart nscd 2>/dev/null || true

echo "== 验证(getent,按 /etc/hosts 优先级) =="
getent ahosts "$DOMAIN" | head -4
