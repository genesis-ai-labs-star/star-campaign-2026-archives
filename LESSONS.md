# LESSONS.md - 失败代码化

_同一错误禁止出现两次。每条教训必须附带防护措施。_

| 日期 | 问题 | 根因 | 修复 | 防护措施 |
|------|------|------|------|----------|
| 2026-02-09 | QQ音乐控制点击落在错误窗口 | 未隐藏其他窗口 | 控制前先隐藏其他窗口 | qqmusic-play.sh 中加入窗口隐藏步骤 |
| 2026-02-18 | weasyprint 无法生成 PDF | 缺少系统依赖 | 改用 fpdf2 | 中文渲染需调试字体路径 |
| 2026-02-20 | gateway 配置变更后不生效 | 旧进程未被杀掉 | 手动 kill 旧进程 | watchdog 在重启时强制 kill 旧 PID |
| 2026-02-22 | session model 字段缓存 | 改配置后 session 缓存未清 | 清空 sessions.json 并重启 gateway | 配置变更后自动清 session 缓存 |
| 2026-02-23 | Claude temperature 挂死 | temperature 必须为 1 + timeout ≥120s | 修正 openclaw.json 参数 | 已在 agents.defaults.models 中固化 |
| 2026-02-25 | contextTokens 过低导致报错 | contextTokens <16000 | 设为 128000 | openclaw.json 中锁定下限 |
| 2026-02-25 | Ollama cloud 模型 401 | 未执行 ollama signin | 执行认证 | 从 main fallback 中移除未认证模型 |
| 2026-02-26 | self-heal.sh 硬编码 sudo 密码 | 快速搭建期遗留 | 删除密码，改为检测+跳过 | GOVERNANCE 第五条禁止硬编码凭据 |
| 2026-02-26 | MEMORY.md 明文存储 API 密钥 | 快速搭建期遗留 | 替换为引用格式 | GOVERNANCE 第二条禁止明文凭据 |

---

_Agent 在 heartbeat 中检查是否有新教训需要编码为防护脚本。_
_此文件通过 sync-dna.sh 同步至所有子 workspace。_
