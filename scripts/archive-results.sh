#!/bin/bash
# scripts/archive-results.sh
# 司令员专用：全矩阵战果自动化归档脚本

ARCHIVE_DIR="/Users/genesis/.openclaw/workspace/campaign-archives"
WORKSPACE_MAIN="/Users/genesis/.openclaw/workspace"
WORKSPACE_INVESTOR="/Users/genesis/.openclaw/workspace-investor"
WORKSPACE_LIFE="/Users/genesis/.openclaw/workspace-life"
WORKSPACE_DEV="/Users/genesis/.openclaw/workspace/Genesis"

echo "🕒 Starting Automated Campaign Archive..."

# 1. Financial Sync
cp $WORKSPACE_INVESTOR/HIT_LIST.md $ARCHIVE_DIR/financial/hit-lists/$(date +%Y-%m-%d)-hit-list.md 2>/dev/null

# 2. Technical Sync
cp -r $WORKSPACE_MAIN/tt-benchmark $ARCHIVE_DIR/technical/benchmarks/ 2>/dev/null
cp $WORKSPACE_MAIN/TT_M4_BENCHMARK_PLAN.md $ARCHIVE_DIR/technical/benchmarks/ 2>/dev/null
cp $WORKSPACE_MAIN/SYSTEM_STANDARDS.md $ARCHIVE_DIR/technical/ 2>/dev/null

# 3. Operations Sync
cp $WORKSPACE_MAIN/GOVERNANCE_2026.md $ARCHIVE_DIR/operations/governance/ 2>/dev/null
cp $WORKSPACE_MAIN/ACTIVE_MISSIONS.json $ARCHIVE_DIR/operations/ 2>/dev/null
cp $WORKSPACE_MAIN/EVOLUTION.md $ARCHIVE_DIR/operations/ 2>/dev/null
cp $WORKSPACE_MAIN/BIOMETRIC_GUARD_PLAN.md $ARCHIVE_DIR/operations/ 2>/dev/null
cp $WORKSPACE_MAIN/memory/$(date +%Y-%m-%d).md $ARCHIVE_DIR/operations/logs/ 2>/dev/null
mkdir -p $ARCHIVE_DIR/operations/logs
cp $WORKSPACE_MAIN/memory/*.md $ARCHIVE_DIR/operations/logs/ 2>/dev/null

# 4. Push to GitHub (Star's Private Repo)
cd $ARCHIVE_DIR
git add .
git commit -m "Automated Archive Update - $(date +'%Y-%m-%d %H:%M')"
git push -u origin main

echo "✅ Archive Complete and Pushed to GitHub."
