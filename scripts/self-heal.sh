#!/bin/bash
# self-heal.sh - 星宝自愈脚本 (Hardened v3 — 无硬编码密码)
# 注意：sudo 操作已移除，需要特权的操作改为检测+跳过+记录

WORKSPACE="/Users/genesis/.openclaw/workspace"
LOG_FILE="/tmp/openclaw_evolution.log"

echo "[$(date)] Starting evolution cycle (v3.0.0 — hardened)..." >> "$LOG_FILE"

# 1. 保持系统唤醒 (不需要 sudo)
if ! pgrep -q caffeinate; then
    echo "[$(date)] Starting caffeinate to prevent sleep..." >> "$LOG_FILE"
    nohup caffeinate -u -i -s -m > /dev/null 2>&1 &
fi

# 2. 修复 Crontab PATH
if ! crontab -l 2>/dev/null | grep -q "PATH=/opt/homebrew/bin"; then
    echo "[$(date)] Crontab PATH missing. Fixing..." >> "$LOG_FILE"
    crontab -l > /tmp/crontab.bak 2>/dev/null || touch /tmp/crontab.bak
    sed -i '' '1i\
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
' /tmp/crontab.bak
    crontab /tmp/crontab.bak && rm /tmp/crontab.bak
fi

# 3. 自动清理僵尸进程 (不需要 sudo)
ps -ef | grep "openclaw" | grep "defunct" | awk '{print $2}' | xargs kill -9 2>/dev/null

# 4. SSH/系统服务状态检查 (仅记录，不尝试 sudo 修复)
if ! pgrep -q sshd; then
    echo "[$(date)] WARN: sshd not running. Manual intervention needed (sudo required)." >> "$LOG_FILE"
fi

echo "[$(date)] Evolution cycle complete." >> "$LOG_FILE"
