#!/bin/bash
# scripts/sync-dna.sh - 意图一致性广播脚本 (Singularity v2)
# 将主 workspace 的核心治理文件同步到所有子 workspace
# 由 watchdog 每小时调用，或在文件变更时手动触发

set -euo pipefail

MAIN="/Users/genesis/.openclaw/workspace"
LOG="/Users/genesis/.openclaw/logs/sync-dna.log"
TARGETS=(
  "/Users/genesis/.openclaw/workspace-investor"
  "/Users/genesis/.openclaw/workspace-life"
)

# 同步的文件（治理核心 — 所有 Agent 必须一致）
SYNC_FILES=(
  "GOVERNANCE.md"
  "LESSONS.md"
)

# 条件同步（仅当目标存在时同步）
SYNC_IF_EXISTS=(
  "STYLE.md"
  "SYSTEM_STANDARDS.md"
)

# 不同步：SOUL.md（各 agent 有自己的灵魂版本）
# 不同步：MEMORY.md（隐私隔离）
# 不同步：ACTIVE_MISSIONS.json（由 main agent 统一管理）

log() {
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [sync-dna] $1" >> "$LOG"
}

sync_count=0
skip_count=0

for target in "${TARGETS[@]}"; do
  if [ ! -d "$target" ]; then
    log "WARN: target workspace not found: $target"
    continue
  fi

  # 核心治理文件必须同步
  for file in "${SYNC_FILES[@]}"; do
    if [ -f "$MAIN/$file" ]; then
      if ! cmp -s "$MAIN/$file" "$target/$file" 2>/dev/null; then
        cp "$MAIN/$file" "$target/$file"
        log "SYNCED: $file -> $target"
        sync_count=$((sync_count + 1))
      else
        skip_count=$((skip_count + 1))
      fi
    else
      log "WARN: source file missing: $MAIN/$file"
    fi
  done

  # 条件同步
  for file in "${SYNC_IF_EXISTS[@]}"; do
    if [ -f "$MAIN/$file" ]; then
      if ! cmp -s "$MAIN/$file" "$target/$file" 2>/dev/null; then
        cp "$MAIN/$file" "$target/$file"
        log "SYNCED: $file -> $target"
        sync_count=$((sync_count + 1))
      else
        skip_count=$((skip_count + 1))
      fi
    fi
  done
done

log "Complete: ${sync_count} files synced, ${skip_count} already up-to-date"
