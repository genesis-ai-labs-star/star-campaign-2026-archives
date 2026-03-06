# AGENTS.md - 星宝单一主权作战体系

> 以 openclaw.json agents.list 为唯一真相源，本文件仅做可读摘要。

## 架构：Grok 调度 + Claude Code 执行

- **路由层**：Grok-4.1-fast（所有 Agent 共用），负责意图识别和任务分发
- **执行层**：Claude Code CLI (Opus 4.6, Max订阅)，通过 ACPX 桥接，负责所有复杂任务
- **专属 Skill**：天气/提醒/邮件/语音等轻量任务，Agent 直接调用对应 skill

## 五大专精 Agent

| Agent | 名称 | 路由模型 | Fallback | 职责 |
|-------|------|----------|----------|------|
| star | 星宝（司令） | xai/grok-4-1-fast-reasoning | gpt-5.2 | 整体调度、安全审计、Agent 编排 |
| dev | 星宝（开发） | xai/grok-4-1-fast-reasoning | gpt-5.2 | 代码/架构/bug 修复/自动化脚本 |
| finance | 星宝（投资） | xai/grok-4-1-fast-reasoning | gpt-5.2 | 美股 AI 赛道研究、产业链逻辑 |
| life | 星宝（生活） | xai/grok-4-1-fast-reasoning | gpt-5.2 | 行程/账单/物流/邮件监控 |
| circle | 星宝（亲友） | xai/grok-4-1-fast-reasoning | gpt-5.2 | 阿桐/俞丽 消息/提醒/计划 |

## 通道绑定

| 通道 | Account | Agent |
|------|---------|-------|
| Telegram | default | star |
| Telegram | invest | finance |
| Telegram | dev | dev |
| Telegram | life | life |
| WhatsApp | default | life |

---
_同步自 openclaw.json，最后更新：2026-03-06_
