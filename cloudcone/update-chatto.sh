#!/bin/bash
# update-chatto.sh —— 开机/手动从 GitHub 抓取 chatto 最新版并重启服务
# 范式同 startup.sh 的 api-pack/azure 段：下载失败降级用现有二进制，不留空窗。
# chatto 是 systemd 管（非 nohup），所以替换后 systemctl restart chatto。
# 2026-10-19 新增；release 资产是 tar.gz（chatto_Linux_x86_64.tar.gz），须解包，不能直接 --dest 二进制路径。

WORK=/opt/chatto
TMPDIR=/tmp/chatto-update

set -u
mkdir -p "$TMPDIR"
rm -f "$TMPDIR"/* 2>/dev/null

echo "[chatto-update] $(date -u +%F\ %T) start"
OLD_VER="$($WORK/chatto version 2>/dev/null | head -1 || echo unknown)"
echo "[chatto-update] current: $OLD_VER"

# 1) 下载 tar.gz（失败即放弃，现有二进制继续跑）
if ! python3 /root/script/download_asset.py --repo Hana-ame/chatto --dest "$TMPDIR/chatto.tar.gz" --pattern chatto_Linux_x86_64.tar.gz; then
  echo "[chatto-update] download FAILED, keep existing binary"; exit 0
fi

# 2) 解包
if ! tar -xzf "$TMPDIR/chatto.tar.gz" -C "$TMPDIR"; then
  echo "[chatto-update] extract FAILED, keep existing binary"; exit 0
fi
if [ ! -x "$TMPDIR/chatto" ]; then
  chmod +x "$TMPDIR/chatto" 2>/dev/null || { echo "[chatto-update] chmod FAILED, keep existing binary"; exit 0; }
fi

# 3) 版本核对：一样就不动（避免每次开机都重启 chatto）
NEW_VER="$("$TMPDIR/chatto" version 2>/dev/null | head -1 || echo unknown)"
echo "[chatto-update] new: $NEW_VER"
if [ "$NEW_VER" = "$OLD_VER" ]; then
  echo "[chatto-update] same version, no restart needed"
  rm -rf "$TMPDIR"
  exit 0
fi

# 4) 原子替换 + 重启
cp "$WORK/chatto" "$WORK/chatto.old.bak" 2>/dev/null   # 留一份回滚（已有 chatto.old.bak 时覆盖）
mv -f "$TMPDIR/chatto" "$WORK/chatto"
chmod +x "$WORK/chatto"
systemctl restart chatto
echo "[chatto-update] replaced and restarted: $OLD_VER -> $NEW_VER"
rm -rf "$TMPDIR"
