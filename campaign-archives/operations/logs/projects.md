# projects.md - 项目层记忆

*最后维护: 2026-03-08 (周维护 by 星宝)*

## [项目: Campaign 2026]
- **目标**：全年净收益 $10,000+，建立 Singularity v3.0 零干预底座。
- **当前状态**：进攻态 (Attack Mode) 已激活。
- **关键里程碑**：
  - [2026-02-09] 星宝首次上线，完成 bootstrap，多渠道通信验证完成。
  - [2026-02-18] Genesis AI MCP Server 端点确认 (`genesis-ai-backend.up.railway.app`)。
  - [2026-02-18] GitHub 品牌账号 `genesis-ai-labs-star` 通过 PAT 登录并验证 SSH key。
  - [2026-02-19] Cap PR #1618 (OPEN)、coolify PR #8456 (CLOSED)、devasignhq PR #56 (OPEN)。
  - [2026-02-20] Devasign #56 代码评分 95/100 (Ready to Merge)。FinMind PR #148 ($50) 提交。
  - [2026-02-24] Expensify PR 流程教训：必须先拿 Assign 再出 PR，凌晨强行提交被秒关。
  - [2026-02-26] M4 基准测试完成：4096x4096 矩阵乘法 1435.90 GFLOPS (Phase 1)。
  - [2026-02-27] M4 vs Tenstorrent 基准测试 Phase 1 完成 (MatMul 3328 GFLOPS)。
  - [2026-02-27] Expensify 赏金猎杀任务按用户指令彻底放弃并归档。
  - [2026-02-27] 战果自动归档系统 (GitHub 私仓 `campaign-2026-archives`) 上线。

## [项目: OpenClaw 演进]
- **目标**：系统自愈与能力扩展。
- **关键进展**：
  - [2026-02-18] Ollama + DeepSeek-R1:7b 作为 fallback 验证可用。
  - [2026-02-20] 本地大模型 (13GB MiniMax) 因 context 超载不可用，彻底卸载。
  - [2026-02-21] 系统更新导致 auth 丢失，已部署 Watchdog 2.0 防护。
  - [2026-02-22] 系统全面修复：contextTokens 8k→128k，fallback 链重构，TTS 配置完成。
  - [2026-02-22] Telegram Bot 更换为 @GenesisInvestBot。
  - [2026-02-26] Agent-Reach 本地部署完成 (YouTube, GitHub, 全网语义搜索)。
  - [2026-02-26] 严格隐私协议实施并验证。
  - **当前状态**：正在集成 Agent-Reach 深度搜索能力。

## [项目: Tenstorrent Matmul 配置引擎]
- **目标**：$2,500 赏金任务。
- **当前状态**：预研/基准测试阶段。M4 基准已建立，待 tt-metal 环境集成。

## [待办]
- [ ] 开启 GitHub 2FA（期限 3月20日）
- [ ] `openclaw doctor --repair` LaunchAgent 配置修复
- [ ] Ollama MiniMax cloud 版 `ollama signin` 认证
- [ ] tt-metal 环境集成 (Tenstorrent 任务)
