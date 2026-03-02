#!/bin/bash
# health-check.sh - Comprehensive system health dashboard for OpenClaw
# Called by daily health dashboard cron job

GATEWAY_URL="http://127.0.0.1:18789/status"
GATEWAY_PID_NAME="openclaw-gateway"
LOG_DIR="/Users/genesis/.openclaw/logs"
OPENCLAW_DIR="/Users/genesis/.openclaw"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

passed=0
warned=0
failed=0

check() {
    local label="$1" status="$2" detail="$3"
    case "$status" in
        ok)   echo -e "[${GREEN}OK${NC}] $label: $detail"; ((passed++)) ;;
        warn) echo -e "[${YELLOW}WARN${NC}] $label: $detail"; ((warned++)) ;;
        fail) echo -e "[${RED}FAIL${NC}] $label: $detail"; ((failed++)) ;;
    esac
}

echo "=============================="
echo " OpenClaw Health Dashboard"
echo " $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=============================="
echo ""

# 1. Gateway process
pid=$(pgrep -f "$GATEWAY_PID_NAME" | head -1)
if [ -n "$pid" ]; then
    mem_rss=$(ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}')
    check "Gateway Process" "ok" "PID $pid, Memory ${mem_rss}MB"
else
    check "Gateway Process" "fail" "Not running"
fi

# 2. Gateway HTTP
http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$GATEWAY_URL" 2>/dev/null)
if [ "$http_code" = "200" ]; then
    check "Gateway HTTP" "ok" "HTTP 200"
elif [ "$http_code" = "000" ]; then
    check "Gateway HTTP" "fail" "Connection refused"
else
    check "Gateway HTTP" "warn" "HTTP $http_code"
fi

# 3. Memory
ps_val=$(pagesize)
free_pages=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
spec_pages=$(vm_stat | grep "Pages speculative" | awk '{print $3}' | sed 's/\.//')
free_mb=$(( (free_pages + spec_pages) * ps_val / 1024 / 1024 ))
if [ "$free_mb" -gt 500 ]; then
    check "Free Memory" "ok" "${free_mb}MB available"
elif [ "$free_mb" -gt 200 ]; then
    check "Free Memory" "warn" "${free_mb}MB available (low)"
else
    check "Free Memory" "fail" "${free_mb}MB available (critical)"
fi

# 4. Disk space
disk_pct=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$disk_pct" -lt 80 ]; then
    check "Disk Usage" "ok" "${disk_pct}% used"
elif [ "$disk_pct" -lt 90 ]; then
    check "Disk Usage" "warn" "${disk_pct}% used"
else
    check "Disk Usage" "fail" "${disk_pct}% used"
fi

# 5. Error counts (last 24h)
echo ""
echo "--- Error Counts (last 24h) ---"
for logfile in "$LOG_DIR"/*.err.log "$LOG_DIR"/*.err; do
    [ -f "$logfile" ] || continue
    count=$(find "$logfile" -mtime -1 -exec wc -l {} \; 2>/dev/null | awk '{print $1}')
    if [ "${count:-0}" -gt 100 ]; then
        check "$(basename "$logfile")" "warn" "$count lines"
    elif [ "${count:-0}" -gt 0 ]; then
        check "$(basename "$logfile")" "ok" "$count lines"
    fi
done

# 6. Rate limiting check
if [ -f "$LOG_DIR/gateway.err.log" ]; then
    rate_limit_count=$(grep -c "rate.limit\|429\|RESOURCE_EXHAUSTED" "$LOG_DIR/gateway.err.log" 2>/dev/null || echo 0)
    if [ "$rate_limit_count" -gt 50 ]; then
        check "Rate Limiting" "fail" "$rate_limit_count occurrences in gateway.err.log"
    elif [ "$rate_limit_count" -gt 10 ]; then
        check "Rate Limiting" "warn" "$rate_limit_count occurrences in gateway.err.log"
    else
        check "Rate Limiting" "ok" "$rate_limit_count occurrences"
    fi
fi

# 7. Cron job health
echo ""
echo "--- Cron Job Health ---"
if [ -f "$OPENCLAW_DIR/cron/jobs.json" ]; then
    python3 -c "
import json
with open('$OPENCLAW_DIR/cron/jobs.json') as f:
    data = json.load(f)
for job in data.get('jobs', []):
    if not job.get('enabled', False):
        continue
    name = job.get('name', 'unknown')
    state = job.get('state', {})
    errors = state.get('consecutiveErrors', 0)
    status = state.get('lastStatus', 'unknown')
    if errors > 3:
        print(f'FAIL|{name}|{errors} consecutive errors')
    elif errors > 0:
        print(f'WARN|{name}|{errors} consecutive errors (last: {status})')
    else:
        print(f'OK|{name}|last status: {status}')
" 2>/dev/null | while IFS='|' read -r level name detail; do
        case "$level" in
            OK)   check "$name" "ok" "$detail" ;;
            WARN) check "$name" "warn" "$detail" ;;
            FAIL) check "$name" "fail" "$detail" ;;
        esac
    done
fi

# 8. Crontab check (should be empty)
crontab_lines=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l | tr -d ' ')
if [ "$crontab_lines" = "0" ] || ! crontab -l >/dev/null 2>&1; then
    check "System Crontab" "ok" "Clean (no entries)"
else
    check "System Crontab" "warn" "$crontab_lines active entries (should be 0)"
fi

# Summary
echo ""
echo "=============================="
echo " Summary: ${passed} passed, ${warned} warnings, ${failed} failures"
echo "=============================="
