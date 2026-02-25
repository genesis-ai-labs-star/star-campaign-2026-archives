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

    # 3. 触发系统级内存清理 (仅清理缓存，不模拟压力)
    # 废弃 memory_pressure -l warn，因为它会分配大量内存导致系统崩溃
    sync && purge


    # 4. 检查系统剩余内存，如果低于 300MB，尝试清理磁盘缓存
    FREE_MEM=$(vm_stat | grep "free" | awk '{print $3}' | sed 's/\.//')
    # vm_stat 输出的是 page count，每页通常是 4096 bytes
    FREE_MB=$((FREE_MEM * 4096 / 1024 / 1024))
    
    if [ "$FREE_MB" -lt 300 ]; then
        echo "$(date) [purger] Critical: Free memory $FREE_MB MB. Purging disk cache..." >> "$LOG_FILE"
        # purge 命令可以安全地清空磁盘缓冲区和未使用的内存页
        sync && purge
    fi

    # 每 5 分钟巡检一次
    sleep 300
done
