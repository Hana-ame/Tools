#!/bin/bash
set -e

SERVERS=("bwh" "vps" "cloudcone")
CERT="/root/.acme.sh/*.d.moonchan.xyz_ecc/fullchain.cer"
KEY="/root/.acme.sh/*.d.moonchan.xyz_ecc/*.d.moonchan.xyz.key"
PORT=8443

SERVICE=$(cat <<'SERVICEEOF'
[Unit]
Description=Zen Proxy
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u /root/zen_proxy.py 0.0.0.0 PORT CERT KEY 30
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICEEOF
)

for srv in "${SERVERS[@]}"; do
    echo "=== $srv ==="

    bash ~/script/ssh/$srv.sh "cat > /root/zen_proxy.py" < /mnt/d/WorkPlace/Tools/zen_proxy.py

echo "$SERVICE" | sed "s|PORT|$PORT|g; s|CERT|$CERT|g; s|KEY|$KEY|g" | \
        bash ~/script/ssh/$srv.sh "cat > /etc/systemd/system/zen.service"

    bash ~/script/ssh/$srv.sh "systemctl daemon-reload && systemctl enable zen && systemctl restart zen"

    bash ~/script/ssh/$srv.sh "journalctl -u zen --no-pager -n 2"
    echo ""
done

echo "All deployed."
