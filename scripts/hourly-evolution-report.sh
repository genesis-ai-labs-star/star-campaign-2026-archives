#!/bin/bash
# hourly-evolution-report.sh - 自动生成小时看板并发送

WORKSPACE="/Users/genesis/.openclaw/workspace"
REPORT_SCRIPT="$WORKSPACE/scripts/generate-report.py"

# 调用 Python 脚本生成格式化报告并发送
python3 $REPORT_SCRIPT
