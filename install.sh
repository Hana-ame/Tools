#!/bin/bash
# zen-multi 一键安装脚本 (Linux + systemd)
# 用法: sudo bash install.sh [PORT]
# 环境变量: BIND_HOST(默认 0.0.0.0) INSTALL_DIR(默认 /opt/zen-multi)
set -euo pipefail

PORT="${1:-8443}"
BIND_HOST="${BIND_HOST:-0.0.0.0}"
INSTALL_DIR="${INSTALL_DIR:-/opt/zen-multi}"
SERVICE="zen-multi"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(command -v python3 || true)"

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: 需要 root (sudo bash $0)"
    exit 1
fi

if [ -z "$PY" ]; then
    echo "ERROR: 未找到 python3"; exit 1
fi

if ss -tln 2>/dev/null | grep -q ":$PORT "; then
    echo "ERROR: 端口 $PORT 已被占用:"
    ss -tlnp | grep ":$PORT " || true
    exit 1
fi

echo "==> [1/4] 复制 zen_multi.py -> $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/zen_multi.py" "$INSTALL_DIR/zen_multi.py"
chmod +x "$INSTALL_DIR/zen_multi.py"

echo "==> [2/4] 准备 Python 环境 (requests)"
VENV_PY=""
if "$PY" -m venv --help >/dev/null 2>&1; then
    if [ ! -d "$INSTALL_DIR/venv" ]; then
        "$PY" -m venv "$INSTALL_DIR/venv" 2>/dev/null && VENV_PY="$INSTALL_DIR/venv/bin/python3" || true
    else
        VENV_PY="$INSTALL_DIR/venv/bin/python3"
    fi
fi

if [ -n "$VENV_PY" ]; then
    "$VENV_PY" -m pip install --quiet --upgrade requests
    RUN_PY="$VENV_PY"
else
    echo "    venv 不可用,回退到 pip install --user"
    "$PY" -m pip install --quiet --user requests 2>/dev/null || {
        apt-get update -qq && apt-get install -y -qq python3-requests
    }
    RUN_PY="$PY"
fi

echo "==> [3/4] 写入 systemd service ($SERVICE)"
cat > "/etc/systemd/system/$SERVICE.service" <<EOF
[Unit]
Description=Zen Multi Proxy (bwh/vps/cloudcone rotate)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$RUN_PY -u $INSTALL_DIR/zen_multi.py $BIND_HOST $PORT
WorkingDirectory=$INSTALL_DIR
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "==> [4/4] 启动并设置开机自启"
systemctl daemon-reload
systemctl enable --now "$SERVICE"
sleep 1

systemctl --no-pager --lines=5 status "$SERVICE"
curl -s "http://$BIND_HOST:$PORT/status" && echo
echo
echo "完成: http://$BIND_HOST:$PORT  (日志: journalctl -u $SERVICE -f)"
