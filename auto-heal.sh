#!/bin/bash
# 星宝“磐石计划”自愈监控脚本
LOG_FILE="/tmp/openclaw-heal.log"
ERR_THRESHOLD=3
ERR_COUNT=0

while true; do
    # 检查 Gateway 进程
    if ! pgrep -f "openclaw gateway" > /dev/null; then
        echo "$(date): Gateway process missing. Restarting..." >> $LOG_FILE
        openclaw gateway restart
    fi

    # 检查是否有全线模型失败的日志记录
    if tail -n 50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | grep -q "All models failed"; then
        ((ERR_COUNT++))
        echo "$(date): Detected all models failed (Count: $ERR_COUNT)" >> $LOG_FILE
    else
        ERR_COUNT=0
    fi

    if [ $ERR_COUNT -ge $ERR_THRESHOLD ]; then
        echo "$(date): Error threshold reached. Force restarting gateway..." >> $LOG_FILE
        openclaw gateway restart
        ERR_COUNT=0
        sleep 60
    fi

    sleep 30
done
