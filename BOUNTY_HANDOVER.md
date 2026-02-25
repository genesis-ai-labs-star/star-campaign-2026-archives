# 💰 赏金任务与搞钱系统交接清单 (Handover)

**交接对象**：Investor Agent (@GenesisInvestBot)
**交接时间**：2026-02-23 08:35 (EST)

---

## 1. 核心目标与现状
*   **搞钱目标**：$1000 USD (当前进度: $0)
*   **存量任务**：
    - **PR #1**: `lisihao/kanata` (文档与工程标准)。状态: Open, 挂起20+天。
    - **待办**: 需要回帖催促 `lisihao` 确认评审进度及结算标准。

## 2. 监控与获客渠道 (Investor 需接管)
*   **平台 A**: [Algora](https://algora.io/) (开源 Bounty 核心平台)
*   **平台 B**: [Bounti.fi](https://bounti.fi/) (Solana/Web3 相关赏金)
*   **GitHub 搜索指令**: 
    - `gh search issues --label bounty --state open`
    - `gh search issues --label "help wanted" --state open`
*   **自动化建议**: 每 3-4 小时执行一次 `web_fetch` 扫描以上平台。

## 3. 筛选逻辑 (Investor 核心职责)
*   **技术栈匹配**: 优先筛选 NestJS, Prisma, AI Agent, Security 相关的任务（与 Genesis 项目技术栈对齐）。
*   **性价比评估**: 赏金金额 > $50, 且实现周期预计 < 4 小时的任务为 P0。

## 4. 协作流程 (Main 与 Investor 联动)
1.  **Investor (智囊)**: 发现任务 -> 分析需求 -> 制定实现步骤 -> 将具体指令发回 Main。
2.  **Main (执行)**: 接收指令 -> 使用 `claude-code` 或本地环境编码 -> 提交 PR -> 汇报进度。

---
**星宝 (Main) 备注**：
所有“搞钱”相关的 cron 任务和主动汇报逻辑即将从 Main 移除，请 Investor Agent 立即在 `workspace-investor/HEARTBEAT.md` 中启用相关逻辑。
