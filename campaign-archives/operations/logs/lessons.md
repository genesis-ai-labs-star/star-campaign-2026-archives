# Lessons / 固化要求（rolling）

## 2026-03-09
- **自主感知世界**：我必须自己定期查看关键渠道（尤其邮箱/GitHub 通知），不能依赖老段提醒。
- **自主决策**：收到外界信号后先判断优先级与下一步动作，给出结论并推进，不把决策压力转移给用户。
- **目标导向**：围绕“赚钱/变现/交付”主线，想尽一切办法推进达成；只在需要用户权限/操作时给最短动作指令。
- **执行风格**：监控→判断→行动→回传结果（简报），减少来回确认。

## 2026-03-15 (Weekly Maintenance)
- **Memory search unavailable**: OpenAI embeddings API key invalid (401 error, ongoing since 03-12).
- **System stability**: Load avg 1.5-1.8, CPU idle >87%, no alerts across week.
- **Cron reliability**: Heartbeats, monetization pipeline, archiving, maintenance tasks self-running.
- **Monetization momentum**: Bounties advancing (rustchain PRs submitted), freelance clues (gold bot/Upwork).
- **Life-ops**: Email delivery issues surfaced — prioritize Gmail bounce resolution.
- **No major breakthroughs**: Routine ops; API key fix + pipeline scale next.
- **Weekly pattern**: Stable ops, persistent config issue (embeddings), no user prefs shifts.

## 2026-03-22 (Weekly Maintenance)
- **OpenAI embeddings key still broken**: 401 error persists since 03-12, now 10 days. memory_search completely unavailable. Must fix or rotate key urgently.
- **System stability excellent**: Full week load avg <2.0, CPU idle >84%, 8 cron jobs zero failures. Gateway had one transient down on 03-18, self-recovered.
- **No user interactions this week**: March 16-21 was entirely autonomous monitoring. No new tasks, no milestones hit.
- **Monetization pipeline steady**: 6+ tracks maintained via hourly refills (rustchain bounties, sorosave issues). No new bounty claims or merges.
- **GitHub 2FA deadline passed**: Was due 03-20, still not enabled. Escalate to user.
- **Claude Code spec-driven delivery validated**: Todo-app (03-16) proved zero-bug single-file generation via spec workflow.
- **Quiet week pattern**: When no user sessions, system runs stable but no forward progress on revenue. Need active bounty push next week.
