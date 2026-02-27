#!/bin/bash
# scripts/skill-doctor.sh - 技能自愈脚本 (Singularity v2)
# 检测缺失技能的依赖并尝试自动修复
# 由 watchdog 每日调用一次

set -euo pipefail

LOG="/Users/genesis/.openclaw/logs/skill-doctor.log"
SKILLS_DIR="/Users/genesis/.openclaw/skills"

log() {
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [skill-doctor] $1" >> "$LOG"
}

log "Starting skill health check..."

# 检查 openclaw 命令是否可用
if ! command -v openclaw &>/dev/null; then
  log "ERROR: openclaw command not found in PATH"
  exit 1
fi

# 运行 openclaw skills check（如果命令存在）
if openclaw skills check &>/dev/null; then
  SKILLS_OUTPUT=$(openclaw skills check 2>&1)
  log "Skills check output: $SKILLS_OUTPUT"
else
  log "WARN: 'openclaw skills check' command not available, falling back to manual check"
fi

# 检查常用命令行工具依赖
BREW_DEPS=(
  "himalaya"
  "gh"
)

fixed=0
missing=0

for dep in "${BREW_DEPS[@]}"; do
  if ! command -v "$dep" &>/dev/null; then
    log "MISSING: $dep not found. Attempting brew install..."
    if brew install "$dep" 2>/dev/null; then
      log "FIXED: $dep installed via brew"
      fixed=$((fixed + 1))
    else
      log "FAIL: could not install $dep"
      missing=$((missing + 1))
    fi
  fi
done

# 检查 Go 工具依赖
GO_DEPS=(
  "mcporter:github.com/nicholasgasior/mcporter@latest"
)

if command -v go &>/dev/null; then
  for entry in "${GO_DEPS[@]}"; do
    cmd="${entry%%:*}"
    pkg="${entry##*:}"
    if ! command -v "$cmd" &>/dev/null; then
      log "MISSING: $cmd not found. Attempting go install..."
      if go install "$pkg" 2>/dev/null; then
        log "FIXED: $cmd installed via go"
        fixed=$((fixed + 1))
      else
        log "FAIL: could not install $cmd"
        missing=$((missing + 1))
      fi
    fi
  done
fi

# 检查 Node.js 全局工具
NODE_DEPS=(
  "clawhub:@openclaw/clawhub"
)

if command -v npm &>/dev/null; then
  for entry in "${NODE_DEPS[@]}"; do
    cmd="${entry%%:*}"
    pkg="${entry##*:}"
    if ! command -v "$cmd" &>/dev/null; then
      log "MISSING: $cmd not found. Attempting npm install..."
      if npm install -g "$pkg" 2>/dev/null; then
        log "FIXED: $cmd installed via npm"
        fixed=$((fixed + 1))
      else
        log "FAIL: could not install $cmd"
        missing=$((missing + 1))
      fi
    fi
  done
fi

log "Complete: ${fixed} fixed, ${missing} still missing"
