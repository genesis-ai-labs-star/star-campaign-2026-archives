#!/bin/bash
# session-cleanup.sh - Automated session and log cleanup for OpenClaw
# Runs daily via cron to prevent unbounded growth of session files
# GOVERNANCE Rule 10: Session retention - interactive 7 days, cron 3 days

set -euo pipefail

OPENCLAW_DIR="$HOME/.openclaw"
AGENTS_DIR="$OPENCLAW_DIR/agents"
CRON_RUNS_DIR="$OPENCLAW_DIR/cron/runs"
MEMORY_DIR="$OPENCLAW_DIR/memory"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Session cleanup starting..."

# 1. Delete interactive session .jsonl files older than 7 days
echo "Cleaning interactive sessions (>7 days)..."
find "$AGENTS_DIR" -name "*.jsonl" -mtime +7 -type f -delete 2>/dev/null
INTERACTIVE_COUNT=$(find "$AGENTS_DIR" -name "*.jsonl" -mtime +7 -type f 2>/dev/null | wc -l | tr -d ' ')
echo "  Remaining old interactive sessions: $INTERACTIVE_COUNT"

# 2. Delete all .jsonl.deleted.* remnants (any age)
echo "Cleaning .jsonl.deleted.* remnants..."
DELETED_COUNT=$(find "$AGENTS_DIR" -name "*.jsonl.deleted.*" -type f 2>/dev/null | wc -l | tr -d ' ')
find "$AGENTS_DIR" -name "*.jsonl.deleted.*" -type f -delete 2>/dev/null
echo "  Removed $DELETED_COUNT deleted session remnants"

# 3. Delete cron isolated session files older than 3 days
echo "Cleaning cron run logs (>3 days)..."
if [ -d "$CRON_RUNS_DIR" ]; then
    CRON_COUNT=$(find "$CRON_RUNS_DIR" -name "*.jsonl" -mtime +3 -type f 2>/dev/null | wc -l | tr -d ' ')
    find "$CRON_RUNS_DIR" -name "*.jsonl" -mtime +3 -type f -delete 2>/dev/null
    echo "  Removed $CRON_COUNT old cron run logs"
fi

# 4. Vacuum SQLite memory stores
echo "Vacuuming SQLite memory stores..."
if [ -d "$MEMORY_DIR" ]; then
    for db in "$MEMORY_DIR"/*.sqlite; do
        if [ -f "$db" ]; then
            sqlite3 "$db" "VACUUM;" 2>/dev/null && echo "  Vacuumed $(basename "$db")" || echo "  Skip $(basename "$db")"
        fi
    done
fi

# 5. Config backup rotation (keep last 7 copies)
echo "Backing up openclaw.json..."
cp /Users/genesis/.openclaw/openclaw.json "/Users/genesis/.openclaw/config_safe/openclaw.json.$(date +%Y%m%d)"
ls -t /Users/genesis/.openclaw/config_safe/openclaw.json.2* 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null
echo "  Config backup rotated (keeping last 7)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Session cleanup complete."
