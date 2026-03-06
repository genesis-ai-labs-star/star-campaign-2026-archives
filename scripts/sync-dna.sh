#!/bin/bash
# scripts/sync-dna.sh - 治理文件符号链接验证器 (Singularity v4)
# 检查所有 workspace 的治理文件 symlink 是否完好，断链时自动修复

set -euo pipefail

SHARED="/Users/genesis/.openclaw/shared-governance"
LOG="/Users/genesis/.openclaw/logs/sync-dna.log"

SYNC_FILES=(
  "GOVERNANCE.md"
  "GOVERNANCE_2026.md"
  "WORKFLOW_AUTO.md"
  "STYLE.md"
  "SYSTEM_STANDARDS.md"
  "LESSONS.md"
)

# target_dir:relative_prefix pairs (macOS bash 3 compatible)
PAIRS=(
  "/Users/genesis/.openclaw/workspace|../shared-governance"
  "/Users/genesis/.openclaw/workspace/Genesis|../../shared-governance"
  "/Users/genesis/.openclaw/workspace-investor|../shared-governance"
  "/Users/genesis/.openclaw/workspace-life|../shared-governance"
  "/Users/genesis/.openclaw/workspace-rel|../shared-governance"
)

log() {
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') [sync-dna] $1" >> "$LOG"
}

ok_count=0
fix_count=0
fail_count=0

for pair in "${PAIRS[@]}"; do
  target="${pair%%|*}"
  rel="${pair##*|}"

  if [ ! -d "$target" ]; then
    log "WARN: target workspace not found: $target"
    continue
  fi

  for file in "${SYNC_FILES[@]}"; do
    link_path="$target/$file"
    expected_target="$rel/$file"

    # Check if it's already a correct symlink
    if [ -L "$link_path" ] && [ "$(readlink "$link_path")" = "$expected_target" ] && [ -r "$link_path" ]; then
      ok_count=$((ok_count + 1))
      continue
    fi

    # Needs repair: remove whatever is there and recreate symlink
    if [ ! -f "$SHARED/$file" ]; then
      log "ERROR: source missing: $SHARED/$file"
      fail_count=$((fail_count + 1))
      continue
    fi

    rm -f "$link_path"
    ln -sf "$expected_target" "$link_path"

    if [ -r "$link_path" ]; then
      log "FIXED: $link_path -> $expected_target"
      fix_count=$((fix_count + 1))
    else
      log "ERROR: failed to fix $link_path"
      fail_count=$((fail_count + 1))
    fi
  done
done

log "Complete: ${ok_count} ok, ${fix_count} fixed, ${fail_count} errors"

if [ "$fail_count" -gt 0 ]; then
  echo "sync-dna: ${fail_count} errors detected, check $LOG" >&2
  exit 1
fi
