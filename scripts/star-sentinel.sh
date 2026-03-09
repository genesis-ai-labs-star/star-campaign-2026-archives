#!/bin/bash
# star-sentinel.sh - v6 - 轻量级辅助守护
# Gateway 存活由 launchd KeepAlive 负责，本脚本补充：
#   1. Gateway HTTP 健康检查（死锁检测）
#   2. 系统内存软清理（不重启 gateway）
#   3. Cron job 健康检查
#   4. Config 完整性守护（防 agent 注入）
#   5. 日志轮转

set -euo pipefail

LOG="/Users/genesis/.openclaw/logs/star-sentinel.log"
OPENCLAW_DIR="/Users/genesis/.openclaw"

GATEWAY_URL="http://127.0.0.1:18789/status"
STALL_FILE="/tmp/sentinel-gateway-stall-count"

log() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [SENTINEL] $1" >> "$LOG"; }

check_gateway_health() {
    local pid=$(pgrep -f "openclaw-gateway")
    if [ -z "$pid" ]; then
        log "WARN: Gateway process not found (launchd should restart)"
        echo 0 > "$STALL_FILE"
        return
    fi

    local mem_rss=$(ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}')
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$GATEWAY_URL" 2>/dev/null || echo "000")

    if [ "$http_code" = "200" ]; then
        log "OK: Gateway healthy (HTTP 200, Mem: ${mem_rss}MB)"
        echo 0 > "$STALL_FILE"
    else
        local stall_count=$(cat "$STALL_FILE" 2>/dev/null || echo 0)
        stall_count=$((stall_count + 1))
        echo "$stall_count" > "$STALL_FILE"
        log "WARN: Gateway HTTP $http_code (stall $stall_count/3, Mem: ${mem_rss}MB)"
        # 连续 3 次失败（3 分钟）才强制重启，避免误杀
        if [ "$stall_count" -ge 3 ]; then
            log "CRITICAL: Gateway unresponsive for 3+ minutes. Force restarting..."
            pkill -9 -f "openclaw-gateway" 2>/dev/null
            sleep 2
            /opt/homebrew/bin/openclaw gateway restart 2>/dev/null || true
            echo 0 > "$STALL_FILE"
        fi
    fi

    # Memory guard: >1.5GB → restart
    if [ -n "$mem_rss" ] && [ "$mem_rss" -gt 1500 ]; then
        log "WARN: Gateway memory ${mem_rss}MB > 1500MB. Restarting..."
        /opt/homebrew/bin/openclaw gateway restart 2>/dev/null || true
    fi
}

# Lane 阻塞检测：扫描 gateway.err.log 最近 5 分钟的 lane wait exceeded，
# 如果 waitedMs > 120000（2分钟），发 SIGUSR1 触发 resetAllLanes()
check_lane_stall() {
    local pid=$(pgrep -f "openclaw-gateway")
    [ -z "$pid" ] && return

    local err_log="$OPENCLAW_DIR/logs/gateway.err.log"
    [ -f "$err_log" ] || return

    # 找最近 5 分钟内 waitedMs > 120000 的 lane wait 事件
    local now=$(date +%s)
    local stalled=$(tail -50 "$err_log" | grep "lane wait exceeded" | while read -r line; do
        # 提取时间戳和 waitedMs
        local ts=$(echo "$line" | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}')
        local waited=$(echo "$line" | grep -oE 'waitedMs=[0-9]+' | cut -d= -f2)
        [ -z "$ts" ] || [ -z "$waited" ] && continue

        # macOS date 解析
        local event_ts=$(date -j -f '%Y-%m-%dT%H:%M:%S' "$ts" +%s 2>/dev/null || echo 0)
        local age=$(( now - event_ts ))

        # 5 分钟内且等待超过 2 分钟
        if [ "$age" -lt 300 ] && [ "$waited" -gt 120000 ]; then
            echo "$line"
        fi
    done)

    if [ -n "$stalled" ]; then
        log "ALERT: Lane stall detected (waitedMs > 120s). Sending SIGUSR1 to reset lanes (pid=$pid)"
        kill -USR1 "$pid" 2>/dev/null || log "WARN: Failed to send SIGUSR1 to gateway"
    fi
}

manage_memory() {
    local ps=$(pagesize)
    local free_pages=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local spec_pages=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | sed 's/\.//')
    local free_mb=$(( (free_pages + spec_pages) * ps / 1024 / 1024 ))

    if [ "$free_mb" -lt 100 ]; then
        log "CRITICAL: Memory ${free_mb}MB. Running purge."
        /usr/sbin/purge 2>/dev/null || log "WARN: purge requires sudo, skipping"
    elif [ "$free_mb" -lt 250 ]; then
        log "WARN: Memory ${free_mb}MB. Soft purge."
        /usr/sbin/purge 2>/dev/null || true
    fi
}

check_config_integrity() {
    cd "$OPENCLAW_DIR"
    if ! git diff --quiet HEAD -- openclaw.json 2>/dev/null; then
        log "ALERT: openclaw.json modified outside config-edit.sh. Rolling back."
        git checkout HEAD -- openclaw.json 2>/dev/null
        chmod 400 openclaw.json
        /opt/homebrew/bin/openclaw gateway restart 2>/dev/null || true
    fi
    # Ensure config stays locked
    local perms=$(stat -f%Lp "$OPENCLAW_DIR/openclaw.json" 2>/dev/null)
    if [ "$perms" != "400" ]; then
        chmod 400 "$OPENCLAW_DIR/openclaw.json"
    fi
}

check_cron_health() {
    local jobs_file="$OPENCLAW_DIR/cron/jobs.json"
    [ -f "$jobs_file" ] || return
    local alerts=$(python3 -c "
import json
with open('$jobs_file') as f:
    data = json.load(f)
for job in data.get('jobs', []):
    if not job.get('enabled', False):
        continue
    errors = job.get('state', {}).get('consecutiveErrors', 0)
    if errors > 3:
        print(f'{job[\"name\"]} ({job[\"id\"][:8]}): {errors} consecutive errors')
" 2>/dev/null)
    if [ -n "$alerts" ]; then
        log "ALERT: Cron jobs failing: $alerts"
    fi
}

rotate_logs() {
    for logfile in "$OPENCLAW_DIR"/logs/*.log; do
        local size=$(stat -f%z "$logfile" 2>/dev/null || echo 0)
        if [ "$size" -gt 5242880 ]; then  # > 5MB
            mv "$logfile" "${logfile}.old"
            : > "$logfile"
            log "Rotated: $(basename "$logfile") (was ${size} bytes)"
        fi
    done
    # Clean old rotated logs and manual snapshots
    find "$OPENCLAW_DIR/logs" -name "*.old" -mtime +3 -delete 2>/dev/null
    find "$OPENCLAW_DIR/logs" -name "*.log.1" -mtime +3 -delete 2>/dev/null
    find "$OPENCLAW_DIR/logs" -name "*.pre-fix-*" -mtime +3 -delete 2>/dev/null
}

main() {
    check_gateway_health
    check_lane_stall
    manage_memory
    check_config_integrity
    check_cron_health
    rotate_logs
}

main
