#!/bin/bash
# OpenClaw Watchdog - 自动检测和恢复所有关键通道
# 每分钟运行一次，通过 launchd 调度

LOG="/Users/genesis/.openclaw/logs/watchdog.log"
GATEWAY_LOG="/Users/genesis/.openclaw/logs/gateway.err.log"
GATEWAY_MAIN_LOG="/Users/genesis/.openclaw/logs/gateway.log"
GATEWAY_PID_NAME="openclaw-gateway"
GATEWAY_PORT=18789
MAX_DISCONNECT_SECONDS=120  # WhatsApp 断连超过2分钟才重启
BLUEBUBBLES_URL="http://localhost:1234"
LOG_MAX_BYTES=5242880  # 5MB per log file
LOG_KEEP=3             # keep 3 rotated copies
MIN_FREE_MEM_MB=200    # alert if free mem < 200MB

log() {
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [watchdog] $1" >> "$LOG"
}

# 1. Gateway 进程存活检查
check_gateway() {
  if ! pgrep -f "$GATEWAY_PID_NAME" > /dev/null 2>&1; then
    log "CRITICAL: gateway process not running. Restarting via launchctl..."
    launchctl bootout gui/501/ai.openclaw.gateway 2>/dev/null
    sleep 1
    launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null
    sleep 10
    if pgrep -f "$GATEWAY_PID_NAME" > /dev/null 2>&1; then
      log "OK: gateway restarted successfully (PID $(pgrep -f "$GATEWAY_PID_NAME" | head -1))"
    else
      log "FAIL: gateway restart failed"
    fi
    return 1
  fi
  return 0
}

# 2. Gateway 端口响应检查 (假死防护：不响应直接重启)
check_gateway_port() {
  if ! curl -s --max-time 10 -o /dev/null "http://127.0.0.1:$GATEWAY_PORT/" 2>/dev/null; then
    log "CRITICAL: gateway port $GATEWAY_PORT not responding (假死). Force restarting..."
    restart_gateway
    return 1
  fi
  return 0
}

# 3. WhatsApp 连接检查
check_whatsapp() {
  local last_wa_activity
  last_wa_activity=$(grep '\[whatsapp\]' /Users/genesis/.openclaw/logs/gateway.log 2>/dev/null | tail -1)

  # 检查是否有 "channel exited" 错误
  local last_exit
  last_exit=$(grep '\[whatsapp\].*channel exited\|Failed sending.*Connection Closed' /Users/genesis/.openclaw/logs/gateway.err.log 2>/dev/null | tail -1)

  if [ -n "$last_exit" ]; then
    # 获取最后一次退出的时间戳
    local exit_ts
    exit_ts=$(echo "$last_exit" | grep -oE '^\S+' | head -1)
    local exit_epoch
    exit_epoch=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%S' "${exit_ts%%.*}" '+%s' 2>/dev/null || echo 0)
    local now_epoch
    now_epoch=$(date '+%s')

    # 检查最后一次成功消息的时间
    local last_ok_ts
    last_ok_ts=$(grep '\[whatsapp\].*\(Sent message\|Inbound message\)' /Users/genesis/.openclaw/logs/gateway.log 2>/dev/null | tail -1 | grep -oE '^\S+' | head -1)
    local last_ok_epoch
    last_ok_epoch=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%S' "${last_ok_ts%%.*}" '+%s' 2>/dev/null || echo 0)

    # 如果最后退出时间 > 最后成功时间，说明 WhatsApp 还没恢复
    if [ "$exit_epoch" -gt "$last_ok_epoch" ]; then
      local disconnect_duration=$((now_epoch - exit_epoch))
      if [ "$disconnect_duration" -gt "$MAX_DISCONNECT_SECONDS" ]; then
        log "CRITICAL: WhatsApp disconnected for ${disconnect_duration}s. Restarting gateway..."
        restart_gateway
        return 1
      else
        log "WARN: WhatsApp disconnected ${disconnect_duration}s ago, waiting..."
      fi
    fi
  fi
  return 0
}

# 4. LLM 连接检查 (Anthropic API)
check_llm() {
  local last_llm_error
  last_llm_error=$(grep -i 'FailoverError\|HTTP 403\|HTTP 429\|HTTP 500\|HTTP 502\|HTTP 503' /Users/genesis/.openclaw/logs/gateway.err.log 2>/dev/null | tail -1)
  if [ -n "$last_llm_error" ]; then
    local err_ts
    err_ts=$(echo "$last_llm_error" | grep -oE '^\S+' | head -1)
    local err_epoch
    err_epoch=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%S' "${err_ts%%.*}" '+%s' 2>/dev/null || echo 0)
    local now_epoch
    now_epoch=$(date '+%s')
    local age=$((now_epoch - err_epoch))
    if [ "$age" -lt 300 ]; then
      log "WARN: LLM error ${age}s ago: $(echo "$last_llm_error" | cut -c 30-120)"
    fi
  fi
  return 0
}

# 重启 gateway (via LaunchAgent)
restart_gateway() {
  log "Stopping gateway via launchctl..."
  launchctl bootout gui/501/ai.openclaw.gateway 2>/dev/null
  sleep 3
  # 确保旧进程已停止
  local pid
  pid=$(pgrep -f "$GATEWAY_PID_NAME" | head -1)
  if [ -n "$pid" ]; then
    log "WARN: old gateway (PID $pid) still alive, force killing..."
    kill -9 "$pid" 2>/dev/null
    sleep 2
  fi
  log "Starting gateway via launchctl..."
  launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null
  sleep 10
  if pgrep -f "$GATEWAY_PID_NAME" > /dev/null 2>&1; then
    log "OK: gateway restarted successfully (PID $(pgrep -f "$GATEWAY_PID_NAME" | head -1))"
  else
    log "FAIL: gateway restart failed!"
  fi
}

# 5. Heap 内存检查（只看最近3分钟内的记录，避免旧日志误触发）
check_heap() {
  local now_epoch
  now_epoch=$(date '+%s')
  local cutoff=$((now_epoch - 180))  # 3分钟前

  # 过滤最近3分钟的 health 日志
  local recent_lines=""
  while IFS= read -r line; do
    local ts
    ts=$(echo "$line" | grep -oE '^[^ ]+' | head -1)
    local line_epoch
    line_epoch=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%S' "${ts%%.*}" '+%s' 2>/dev/null || echo 0)
    if [ "$line_epoch" -ge "$cutoff" ]; then
      recent_lines="${recent_lines}${line}"$'\n'
    fi
  done < <(grep '\[health\].*heap at' "$GATEWAY_LOG" 2>/dev/null | tail -10)

  if [ -z "$recent_lines" ]; then
    return 0
  fi

  # 取最新一条的百分比
  local last_heap
  last_heap=$(echo "$recent_lines" | tail -2 | head -1)
  local pct
  pct=$(echo "$last_heap" | grep -oE 'heap at ([0-9]+)%' | grep -oE '[0-9]+')
  if [ -z "$pct" ]; then
    return 0
  fi

  if [ "$pct" -ge 95 ]; then
    # 统计最近记录中>=90%的条数
    local total
    total=$(echo "$recent_lines" | grep -c '\[health\]')
    local high_count
    high_count=$(echo "$recent_lines" | grep -cE 'heap at (9[0-9]|100)%')
    if [ "$high_count" -ge 3 ]; then
      log "CRITICAL: heap at ${pct}% sustained (${high_count}/${total} recent checks >=90%). Force restarting gateway..."
      restart_gateway
      return 1
    else
      log "WARN: heap at ${pct}% but not sustained yet (${high_count}/${total} recent checks >=90%)"
    fi
  fi
  return 0
}

# 6. BlueBubbles 连接检查
check_bluebubbles() {
  # 检查 BlueBubbles server 是否可达
  if ! curl -s --max-time 5 -o /dev/null "$BLUEBUBBLES_URL" 2>/dev/null; then
    log "WARN: BlueBubbles server not responding at $BLUEBUBBLES_URL"
    return 1
  fi

  # 检查 gateway 日志中 BlueBubbles 最近是否有错误
  local last_bb_error
  last_bb_error=$(grep '\[bluebubbles\].*error\|BlueBubbles.*fail\|BlueBubbles.*disconnect' "$GATEWAY_LOG" 2>/dev/null | tail -1)
  if [ -n "$last_bb_error" ]; then
    local err_ts
    err_ts=$(echo "$last_bb_error" | grep -oE '^\S+' | head -1)
    local err_epoch
    err_epoch=$(TZ=UTC date -j -f '%Y-%m-%dT%H:%M:%S' "${err_ts%%.*}" '+%s' 2>/dev/null || echo 0)
    local now_epoch
    now_epoch=$(date '+%s')
    local age=$((now_epoch - err_epoch))
    if [ "$age" -lt 300 ]; then
      log "WARN: BlueBubbles error ${age}s ago: $(echo "$last_bb_error" | cut -c 30-120)"
    fi
  fi
  return 0
}

# 7. 系统内存监控
check_system_memory() {
  local free_mem
  free_mem=$(vm_stat 2>/dev/null | awk '/Pages free/ {free=$3} /Pages speculative/ {spec=$3} END {gsub(/\./,"",free); gsub(/\./,"",spec); print int((free+spec)*4096/1048576)}')
  if [ -z "$free_mem" ] || [ "$free_mem" -eq 0 ]; then
    # fallback: parse from top
    free_mem=$(top -l 1 -n 0 -s 0 2>/dev/null | grep PhysMem | grep -oE '([0-9]+)M unused' | grep -oE '[0-9]+')
  fi

  if [ -n "$free_mem" ] && [ "$free_mem" -lt "$MIN_FREE_MEM_MB" ]; then
    log "CRITICAL: system free memory only ${free_mem}MB (threshold: ${MIN_FREE_MEM_MB}MB). Restarting gateway to reclaim memory..."
    purge 2>/dev/null
    restart_gateway
    return 1
  fi
  return 0
}

# 8. 日志轮转
rotate_log() {
  local logfile="$1"
  if [ ! -f "$logfile" ]; then
    return 0
  fi
  local size
  size=$(stat -f%z "$logfile" 2>/dev/null || echo 0)
  if [ "$size" -gt "$LOG_MAX_BYTES" ]; then
    # 删除最旧的，移动现有的
    local i=$LOG_KEEP
    while [ "$i" -gt 1 ]; do
      local prev=$((i - 1))
      [ -f "${logfile}.${prev}" ] && mv "${logfile}.${prev}" "${logfile}.${i}"
      i=$prev
    done
    mv "$logfile" "${logfile}.1"
    touch "$logfile"
    log "rotated $logfile (was ${size} bytes)"
  fi
}

rotate_logs() {
  rotate_log "$GATEWAY_MAIN_LOG"
  rotate_log "$GATEWAY_LOG"
  rotate_log "$LOG"
}

# 9. Auth profile 自动恢复（防止认证漂移）
check_auth_profiles() {
  local active="/Users/genesis/.openclaw/agents/main/agent/auth-profiles.json"
  local safe="/Users/genesis/.openclaw/config_safe/auth-profiles.json"
  if [ ! -s "$active" ]; then
    if [ -s "$safe" ]; then
      cp "$safe" "$active"
      log "AUTH_RESTORED: copied safe auth-profiles.json to active"
    else
      log "CRITICAL: both active and safe auth-profiles.json are empty/missing!"
    fi
  fi
}

# 主逻辑
main() {
  rotate_logs
  check_auth_profiles
  check_gateway || exit 0  # gateway 不在就直接重启，不用查别的
  check_gateway_port || exit 0  # 端口不通已重启，跳过后续
  check_heap
  check_whatsapp
  check_bluebubbles
  check_llm
  check_system_memory
}

main
