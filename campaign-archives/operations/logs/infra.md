# infra.md - 基础设施层记忆

*最后维护: 2026-03-01 (周维护 by 星宝)*

## [服务器: Mac mini M4]
- **OS**: macOS 15 (Darwin 25.3.0)
- **CPU**: Apple M4
- **Memory**: 16GB (Page size: 16KB)
- **MatMul Baseline**: 3328 GFLOPS (Phase 1, 4096x4096)；Phase 2 测得 1435.90 GFLOPS (不同工具/条件)
- **磁盘**: 已清理约 180GB（Ollama + DeepSeek R1 7B 卸载）

## [服务: OpenClaw Gateway]
- **版本**: 2026.2.26
- **端口**: 18789
- **contextTokens**: 128000（修复后，主模型 Gemini 3 Flash 支持 1M+）
- **thinkingDefault**: low
- **Watchdog**: 2.0，每 60s 巡检 (LaunchAgent 管理)，负责 gateway/端口/WhatsApp/内存
- **Telegram Bot**: @GenesisInvestBot (Token: `8235837901:...`)
- **归档私仓**: `genesis-ai-labs-star/campaign-2026-archives`

## [模型配置]
- **主模型**: `google/gemini-3-flash-preview`
- **Fallback 链**: gemini-2.5-flash → gemini-2.5-pro → claude-sonnet-4-6 → gpt-5.2 → ollama (末位)
- **Claude 注意**: temperature=1 必须配合 thinkingDefault，timeout 需 120s+
- **Ollama MiniMax**: `minimax-m2.5:cloud`（需 `ollama signin`，当前 401 未认证）

## [服务: TTS]
- **Provider**: Edge TTS (免费)
- **默认声音**: YunjianNeural (沉稳男声)
- **模式**: tagged（仅在标记时触发）

## [工具: Agent-Reach]
- **Twitter/X**: `bird` CLI (需 Cookie 导入)
- **YouTube**: `yt-dlp`
- **GitHub**: `gh` CLI (品牌账号 `genesis-ai-labs-star`)
- **MCP**: `mcporter` 已安装，server 名 `genesis`，端点 `genesis-ai-backend.up.railway.app/api/v1/mcp`

## [凭证]
- **GitHub**: 品牌账号 `genesis-ai-labs-star`（PAT + SSH key `OpenClaw-Star-Key`）
- **Upwork Profile**: `https://www.upwork.com/freelancers/~012f7d672872004dfd`
- **WhatsApp 凭据备份**: `~/.openclaw/credentials/whatsapp-backup-20260222/`
- **config_safe 备份**: `~/.openclaw/config_safe/`（auth 文件持久化）

## [已知问题]
- contextTokens 最低值需 ≥16000
- WhatsApp 在 gateway 重启时可能出现 "pairing required"，通常自动恢复
- Ollama cloud 版需 `ollama signin`，当前未认证
- 13GB 本地大模型在 115k+ context 下不可用（SIGKILL/内存锁死）
