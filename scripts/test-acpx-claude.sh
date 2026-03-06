#!/bin/bash
# End-to-end test: acpx -> claude-agent-acp -> Claude Code CLI
set -e

ACPX_CMD="node /opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/acpx/dist/cli.js"

echo "=== Test 1: Claude CLI direct ==="
claude -p "respond with just: ACPX_TEST_OK" --output-format text 2>&1
echo ""

echo "=== Test 2: acpx -> claude adapter ==="
$ACPX_CMD --verbose --approve-all --timeout 30 claude exec "respond with just: ACPX_BRIDGE_OK" 2>&1
echo ""

echo "=== Test 3: OpenClaw ACP client ==="
openclaw acp client 2>&1 | head -20
echo ""

echo "=== All tests complete ==="
