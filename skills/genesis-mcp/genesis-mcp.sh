#!/usr/bin/env bash
set -euo pipefail
CFG="${OPENCLAW_MCPORTER_CONFIG:-$HOME/.openclaw/config/mcporter.json}"
mcporter --config "$CFG" "$@"
