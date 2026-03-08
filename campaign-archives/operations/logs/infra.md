# infra.md - 基础设施层记忆

*最后维护: 2026-03-08 (周维护 by 星宝)*

## [服务器: Mac mini M4]
- **OS**: macOS 15 (Darwin 25.3.0)
- **CPU**: Apple M4
- **Memory**: 16GB (Page size: 16KB)
- **MatMul Baseline**: 3328 GFLOPS (Phase 1, 4096x4096)；Phase 2 测得 1435.90 GFLOPS (不同工具/条件)
- **磁盘**: 已清理约 180GB（Ollama + DeepSeek R1 7B 卸载）

## [服务: OpenClaw Gateway]
- **版本**: 2026.3.2
- **端口**: 18789
- **contextTokens**: 32768 (当前记录；历史上曾扩到 128k 做过全量修复)
- **thinkingDefault**: low
- **sandbox**: off（已清理旧 sandbox 容器）
- **Watchdog**: 2.0，每 60s 巡检 (LaunchAgent 管理)，负责 gateway/端口/WhatsApp/内存
- **Telegram Bot**: @GenesisInvestBot (Token: `8235837901:...`)
- **归档私仓**: `genesis-ai-labs-star/campaign-2026-archives`

## [模型配置]（以 openclaw.json 为准）
- **已配置 providers**: xai (grok-4-1-fast-reasoning), openai (gpt-5.2), ollama (qwen3.5:9b)
- **各 agent 主模型/fallback 见 AGENTS.md**
- **智能路由**: smart-router 插件在网关层按 prompt 内容动态覆盖（详见下方 [插件: Smart Router]）
- **Claude 注意**: temperature=1 必须配合 thinkingDefault，timeout 需 120s+

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

## [插件: Smart Router]
- **路径**: `~/openclaw-smart-router/`
- **Hook**: `before_model_resolve` (priority 50)，网关层拦截，对 agent 透明
- **原理**: 纯关键词/正则分类（<1ms），不调用 LLM，按任务类型+复杂度自动选模型
- **Tier 映射**:

| Tier | 模型 | 触发场景 |
|------|------|----------|
| fast | `ollama/qwen3.5:9b` | 简单对话、问答、简单翻译/摘要 |
| balanced | `openai/gpt-5.2` | 编程(简单)、创意写作、中等翻译/分析 |
| powerful | `openai/gpt-5.2` | 复杂编程、复杂分析、复杂创意写作 |
| reasoning | `xai/grok-4-1-fast-reasoning` | 数学推理、证明、逻辑推导 |
| vision | `openai/gpt-5.2` | 图片理解 |
| code | `openai/gpt-5.2` | 规则覆盖时触发 |

- **分类类型**: coding, creative_writing, analysis, translation, math_reasoning, simple_qa, image_understanding, summarization, conversation
- **优先级模式**: balanced（当前）；可选 cost（降级）/ quality（升级）
- **置信度阈值**: 0.3，低于此值 fall through 到 agent 默认模型
- **日志**: `logDecisions: true`，所有路由决策写入网关日志
- **状态**: 已生效，日志可见 `[hooks] model overridden to ...`
- **配置位置**: `~/.openclaw/openclaw.json` → `plugins.entries.smart-router.config`
- **注意**: 这是网关层插件，agent 不需要也无法直接操控它；它在 agent 选模型之前介入

## [已知问题]
- contextTokens 最低值需 ≥16000
- WhatsApp 在 gateway 重启时可能出现 "pairing required"，通常自动恢复
- Ollama cloud 版需 `ollama signin`，当前未认证
- 13GB 本地大模型在 115k+ context 下不可用（SIGKILL/内存锁死）
