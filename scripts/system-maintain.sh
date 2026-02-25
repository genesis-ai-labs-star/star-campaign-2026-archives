#!/bin/bash
# === macOS System Maintenance Script ===
# Run weekly: maintains performance on 8GB MacBook Pro 2015
# Usage: bash ~/.openclaw/workspace/scripts/system-maintain.sh

echo "=== macOS System Maintenance ==="
echo "Started: $(date)"
echo ""

# 1. Memory cleanup
echo "[1/8] Purging inactive memory..."
sudo purge 2>/dev/null && echo "  Done" || echo "  Skipped (no sudo)"

# 2. DNS cache flush
echo "[2/8] Flushing DNS cache..."
sudo dscacheutil -flushcache 2>/dev/null
sudo killall -HUP mDNSResponder 2>/dev/null
echo "  Done"

# 3. System logs cleanup
echo "[3/8] Cleaning system logs..."
sudo rm -rf /private/var/log/asl/*.asl 2>/dev/null
sudo rm -rf /private/var/log/*.gz 2>/dev/null
rm -rf ~/Library/Logs/DiagnosticReports/* 2>/dev/null
echo "  Done"

# 4. QuickLook cache
echo "[4/8] Clearing QuickLook cache..."
qlmanage -r cache 2>/dev/null | tail -1
echo "  Done"

# 5. Brew cleanup
echo "[5/8] Cleaning Homebrew cache..."
brew cleanup --prune=7 2>/dev/null | tail -1
echo "  Done"

# 6. pip cache
echo "[6/8] Cleaning pip cache..."
pip3 cache purge 2>/dev/null | tail -1
echo "  Done"

# 7. npm cache
echo "[7/8] Cleaning npm cache..."
npm cache clean --force 2>/dev/null | tail -1
echo "  Done"

# 8. System status report
echo "[8/8] System status:"
echo "  Memory: $(vm_stat | awk '/Pages free/{printf "%.0f MB free", $3*4/1024}')"
echo "  Swap: $(sysctl vm.swapusage | awk '{print $4, $5}')"
echo "  Disk: $(df -h / | awk 'NR==2{print $4 " available"}')"
echo "  Load: $(sysctl -n vm.loadavg)"

echo ""
echo "=== Maintenance Complete: $(date) ==="
