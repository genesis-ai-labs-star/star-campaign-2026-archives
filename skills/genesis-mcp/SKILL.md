---
name: genesis-mcp
description: Call your Genesis AI MCP server (Railway) via mcporter.
metadata:
  {
    "openclaw": {
      "emoji": "🧬",
      "requires": { "bins": ["mcporter"] }
    }
  }
---

# Genesis MCP (Railway)

This skill routes tool calls to your Genesis AI MCP server.

## Config

This skill expects mcporter config at:

- `~/.openclaw/config/mcporter.json`

with a server named `genesis`.

## Quick test

```bash
mcporter --config ~/.openclaw/config/mcporter.json list genesis --schema
```

## Call a tool

```bash
mcporter --config ~/.openclaw/config/mcporter.json call genesis.genesis_ask question='AI算力接下来一年最大的变量是什么？'
```

## Deep research

```bash
mcporter --config ~/.openclaw/config/mcporter.json call genesis.genesis_deep_research \
  topic='AI算力趋势（2026）' depth=quick language=zh-CN
```
