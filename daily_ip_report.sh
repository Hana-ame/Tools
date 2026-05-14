#!/bin/bash
# 每日凌晨拉取各服务器日志，生成 IP 统计报告并上传
# cron: 0 4 * * * /mnt/d/WorkPlace/tools/daily_ip_report.sh

set -e
TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="/mnt/d/WorkPlace"
STAMP=$(date +%Y%m%d_%H%M)

log() { echo "[$(date '+%H:%M:%S')] $*"; }

# ── VPS (Twitter) ──────────────────────────────────────────
log "VPS: 拉取 Twitter 日志..."
ssh -o ConnectTimeout=15 root@vps.moonchan.xyz \
    "grep '\[GIN\]' /root/twitter/nohup.out | gzip" \
    > "/tmp/vps_gin_${STAMP}.log.gz" 2>/dev/null && {
    log "VPS: 分析中..."
    python3 "$TOOLS_DIR/twitter_stats.py" "/tmp/vps_gin_${STAMP}.log.gz" \
        -o "$WORK_DIR" -n vps --mode api
    python3 "$HOME/.claude/skills/gzip-uploader/scripts/upload.py" \
        "$WORK_DIR/vps_daily_stats.html" "vps_daily_stats.html" >/dev/null
    rm "/tmp/vps_gin_${STAMP}.log.gz"
    log "VPS: 完成"
} || log "VPS: 失败 (跳过)"

# ── Cloudcone (漫画站) ─────────────────────────────────────
log "Cloudcone: 拉取日志..."
scp -o ConnectTimeout=15 root@cloudcone.moonchan.xyz:/root/nohup.out \
    "/tmp/cloudcone_${STAMP}.log" 2>/dev/null && {
    log "Cloudcone: 分析中..."
    python3 "$TOOLS_DIR/twitter_stats.py" "/tmp/cloudcone_${STAMP}.log" \
        -o "$WORK_DIR" -n cloudcone --mode comic
    python3 "$HOME/.claude/skills/gzip-uploader/scripts/upload.py" \
        "$WORK_DIR/cloudcone_daily_stats.html" "cloudcone_daily_stats.html" >/dev/null
    rm "/tmp/cloudcone_${STAMP}.log"
    log "Cloudcone: 完成"
} || log "Cloudcone: 失败 (跳过)"

log "全部完成"
