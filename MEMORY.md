# MEMORY.md - 星宝的长期记忆

_只在主会话中加载。群聊、共享上下文中不读取此文件。_

## 用户
- 段俊杰 (Junjie Duan)，常驻加拿大渥太华 (Ottawa/Nepean)
- 中文为主，英文流利
- 风格：直接、简洁、行动导向。说"一次性全部搞定"就真的要全搞定
- AI + 安全全栈工程师
- 投资关注：美股 AI 算力全产业链（能源→芯片→网络→模型→应用），产业链逻辑派
- 喜欢陈奕迅的歌

## 联系人
- 段俊杰 - hello.junjie.duan@gmail.com
- 俞丽 - lucky.lee.yu@gmail.com
- 俞丽 - WhatsApp: +16138622927
- 阿桐 - WhatsApp: +16139837666
- 详见 contacts.md

## 消息格式偏好
- WhatsApp 上不要用 markdown 格式（手机端显示混乱）
- 用纯文本+简单换行
- 不要发技术过程细节，只发关键结果
- 任务必须闭环完成，不要半途而废

## 已配置通道
- WhatsApp（+13433686913）
- Telegram（@GenesisInvestBot — 凭据存储在 openclaw credentials 中）
- iMessage（已禁用）

## 邮件配置（2026-02-18）
- Gmail：hello.junjie.duan@gmail.com — 凭据存储在 openclaw credentials 中
- Foxmail：hello.duan@foxmail.com — 凭据存储在 openclaw credentials 中
- 发送方式：Python smtplib（详见 workspace/email-config.md）
- himalaya 未安装，用 Python 脚本替代

## 模型配置 (2026-02-25 更新)
- 主模型：google/gemini-3-flash（速度优先）
- 本地模型：ollama/qwen2.5-coder:7b (当前唯一已安装本地模型)
- 待安装/备选：ollama/deepseek-r1:14b (记录显示曾作为主力，但当前本地实际未安装)
- 备用链：gemini-2.5-flash → claude-sonnet-4-6 → gpt-5.1
- contextTokens: 128000

## 当前环境
- Mac mini (Apple Silicon M4), macOS 26.3 (Darwin 25.3.0)
- OpenClaw 2026.2.21-2, Gateway port 18789
- Claude Code v2 (/opt/homebrew/bin/claude)
- Node.js 25.6.1
- GitHub CLI (gh) 已安装，已登录 JUNJIE-DUAN

## 任务与阻塞 (2026-02-26 更新)
- **Upwork/Expensify**: 已彻底放弃。禁止在任何报告或任务中提及 Upwork 或 Expensify。相关资源已全部释放。
- **GitHub 2FA**: 开启截止日期 3月20日。
- **Tenstorrent**: 当前主攻方向，正在编写性能基准测试脚本。

## 已知问题
- macOS 上 openclaw gateway stop 有时不杀老进程，需要手动 kill
- Claude Code 订阅 token 不支持标准 Anthropic API 调用
- session 文件里的 model 字段是缓存，改配置后需要清空 sessions.json 并重启 gateway
- contextTokens 不能低于 16000，否则所有模型报 "context window too small"
- WhatsApp 在 gateway 重启期间会短暂断连（pairing required），通常自动恢复
- Ollama cloud 模型需要 ollama signin 认证，否则 401 Unauthorized
- **Claude temperature=1 陷阱**：Claude 的 temperature 必须为 1 才能配合推理模式，且 timeout 必须设 ≥120s，否则挂死无响应
- BlueBubbles (localhost:1234) 每分钟产生 WARN 日志，属预期（iMessage 禁用），可忽略

## 回复格式与视觉规范
- 严格遵循 `STYLE.md` 中的 Telegram 和 Email 输出协议。
- Telegram：垂直对齐、粗细有别、模块化、整句加粗重点。
- Email：专业 Dashboard 风格、移动端适配、发送者名为“星宝”、标题带时间。
- 邮件目标：hello.duan@foxmail.com。
- 署名：每条回复末尾署名：— 星宝 (实际使用的模型名)。

## 从旧环境迁移的遗产 (2026-02-09)
- 系统优化经验：负载优化、磁盘清理、动画关闭等
- Watchdog 自愈体系设计（进程监控、heap检查、WhatsApp断连检测）
- QQ音乐控制脚本
- system-maintain.sh 系统维护脚本

## 教训
- QQ音乐控制时必须先隐藏其他窗口，否则点击会落在错误窗口
- 用户催促时先汇报进度，别闷头干
- PDF生成：weasyprint缺系统依赖，fpdf2可用但中文渲染需调试
- 不要发重复内容
- gateway 配置变更后必须确认旧进程被杀掉，否则新配置不生效

---
_最后更新：2026-02-26_
