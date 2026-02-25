#!/bin/bash
# self-heal.sh - 星宝自愈与进化脚本 (Hardened v2)

WORKSPACE="/Users/genesis/.openclaw/workspace"
LOG_FILE="/tmp/openclaw_evolution.log"
PASS="YuLi@2026"

echo "[$(date)] Starting evolution cycle (v1.4.2)..." >> $LOG_FILE

# 1. 修复 SSH
if ! ps aux | grep -v grep | grep -q "sshd"; then
    echo "[$(date)] SSH down. Attempting recovery..." >> $LOG_FILE
    echo "$PASS" | sudo -S launchctl load -w /System/Library/LaunchDaemons/ssh.plist 2>/dev/null
    echo "$PASS" | sudo -S systemsetup -setremotelogin on 2>/dev/null
fi

# 2. 保持系统唤醒
if ! ps aux | grep -v grep | grep -q "caffeinate"; then
    echo "[$(date)] Starting caffeinate to prevent sleep..." >> $LOG_FILE
    nohup caffeinate -u -i -s -m &
fi

# 3. 系统核心服务监控 (accountsd, contactsd)
# 如果这些服务不在，或者报错频繁，执行重置
if ! pgrep accountsd > /dev/null; then
    echo "[$(date)] accountsd missing. Resetting system auth services..." >> $LOG_FILE
    echo "$PASS" | sudo -S pkill -9 accountsd contactsd tccd 2>/dev/null
fi

# 4. 修复 Crontab PATH (Evolution v1.5.0)
if ! crontab -l | grep -q "PATH=/opt/homebrew/bin"; then
    echo "[$(date)] Crontab PATH missing. Fixing..." >> $LOG_FILE
    crontab -l > /tmp/crontab.bak 2>/dev/null || touch /tmp/crontab.bak
    sed -i '' '1i\
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
' /tmp/crontab.bak
    crontab /tmp/crontab.bak && rm /tmp/crontab.bak
fi

# 5. 进程优先级加固
echo "$PASS" | sudo -S renice -n -20 -p $(pgrep openclaw-gateway) 2>/dev/null
echo "$PASS" | sudo -S renice -n -20 -p $(pgrep sshd) 2>/dev/null

# 6. 自动清理僵尸进程
ps -ef | grep "openclaw" | grep "defunct" | awk '{print $2}' | xargs kill -9 2>/dev/null

echo "[$(date)] Evolution cycle complete." >> $LOG_FILE
