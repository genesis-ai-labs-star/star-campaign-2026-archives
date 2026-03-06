#!/bin/bash
# memory-purger.sh - 星宝的内存守护进程
# 目标：定期清理僵尸进程和释放无效内存，确保 Mac mini 搞钱环境丝滑

LOG_FILE="$HOME/.openclaw/logs/memory-purger.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date) [purger] Memory Purger started." >> "$LOG_FILE"

while true; do
    # 1. 强杀残留的 claude 进程 (如果超过 1 小时没活动)
    # 简单起见，先杀掉所有非当前活跃的 claude 进程
    # (这里可以根据需求精细化，目前先暴力清理以确保内存)
    # pkill -9 -f "claude" 

    # 2. 发现并清理占用内存过高 (>800MB) 的 WebKit/Safari 僵尸进程
    # 这些通常是后台网页泄露
    ps -A -o pid,rss,comm | grep "WebKit" | while read -r pid rss comm; do
        if [ "$rss" -gt 800000 ]; then
            echo "$(date) [purger] Killing bloated WebKit process: $pid (RSS: $rss)" >> "$LOG_FILE"
            kill -9 "$pid"
        fi
    done

    # 3. 检查系统剩余内存，仅在低于阈值时 purge（watchdog 已有每分钟检查）
    FREE_PAGES=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    SPEC_PAGES=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | sed 's/\.//')
    PAGE_SIZE=$(pagesize)
    FREE_MB=$(( (FREE_PAGES + SPEC_PAGES) * PAGE_SIZE / 1024 / 1024 ))

    if [ "$FREE_MB" -lt 200 ]; then
        echo "$(date) [purger] Low memory: ${FREE_MB}MB free. Purging..." >> "$LOG_FILE"
        sync && /usr/sbin/purge
    fi

    # 每 30 分钟巡检一次（Mac 上 500MB free 是正常的，无需频繁检查）
    sleep 1800
done
