#!/bin/bash
# star-sentinel.sh - v3 - 融合 watchdog + sentinel
# 目标：M4 架构下自适应自愈、资源管理、Gateway 健康检查

LOG="/Users/genesis/.openclaw/logs/star-sentinel.log"
GATEWAY_URL="http://127.0.0.1:18789/status"
GATEWAY_PID_NAME="openclaw-gateway"
MAX_MEMORY_MB=1500

log() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [SENTINEL] $1" >> "$LOG"; }

check_hardware() {
    local chip=$(/usr/sbin/system_profiler SPHardwareDataType 2>/dev/null | grep "Chip" | awk -F': ' '{print $2}')
    log "Hardware: $chip (PageSize: $(pagesize))"
}

manage_memory() {
    local ps=$(pagesize)
    local free_pages=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local spec_pages=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | sed 's/\.//')
    local free_mb=$(( (free_pages + spec_pages) * ps / 1024 / 1024 ))

    if [ "$free_mb" -lt 200 ]; then
        log "CRITICAL: Memory ${free_mb}MB. Attempting purge + gateway restart."
        /usr/sbin/purge 2>/dev/null || log "WARN: purge requires sudo, skipping"
        launchctl bootout gui/501/ai.openclaw.gateway 2>/dev/null || true
        sleep 2
        launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
    elif [ "$free_mb" -lt 500 ]; then
        log "WARN: Memory ${free_mb}MB. Soft purge."
        /usr/sbin/purge 2>/dev/null || true
    fi
}

lockdown_processes() {
    local pid=$(pgrep -f "$GATEWAY_PID_NAME" | head -1)
    [ -n "$pid" ] && renice -20 -p "$pid" > /dev/null 2>&1
}

check_gateway_health() {
    local pid=$(pgrep -f "$GATEWAY_PID_NAME" | head -1)
    if [ -z "$pid" ]; then
        log "ERROR: Gateway not found. Restarting..."
        /opt/homebrew/bin/openclaw gateway restart 2>/dev/null
        return
    fi
    local mem_rss=$(ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}')
    if [ "${mem_rss:-0}" -gt "$MAX_MEMORY_MB" ]; then
        log "WARNING: Gateway ${mem_rss}MB > ${MAX_MEMORY_MB}MB. Restarting..."
        /opt/homebrew/bin/openclaw gateway restart 2>/dev/null
        return
    fi
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$GATEWAY_URL")
    if [ "$http_code" != "200" ]; then
        log "ERROR: Health check failed (HTTP $http_code). Force restarting..."
        pkill -9 -f "$GATEWAY_PID_NAME" 2>/dev/null || true
        sleep 2
        /opt/homebrew/bin/openclaw gateway restart 2>/dev/null
    else
        log "OK: Gateway healthy (HTTP 200, Mem: ${mem_rss:-?}MB)"
    fi
}

check_cron_health() {
    local jobs_file="/Users/genesis/.openclaw/cron/jobs.json"
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
    for logfile in /Users/genesis/.openclaw/logs/*.log; do
        local size=$(stat -f%z "$logfile" 2>/dev/null || echo 0)
        if [ "$size" -gt 5242880 ]; then  # > 5MB
            mv "$logfile" "${logfile}.old"
            : > "$logfile"
            log "Rotated: $(basename "$logfile") (was ${size} bytes)"
        fi
    done
    find /Users/genesis/.openclaw/logs -name "*.old" -mtime +7 -delete 2>/dev/null
    find /Users/genesis/.openclaw/logs -name "*.log.1" -mtime +7 -delete 2>/dev/null
}

main() {
    check_hardware
    manage_memory
    lockdown_processes
    check_gateway_health
    check_cron_health
    rotate_logs
}

main
