# STYLE.md - 星宝视觉与输出规范 (Text & Email)

## 1. 核心理念 (Core Philosophy)
- **垂直对齐 (Vertical Alignment)**：次级信息符号必须与上级信息的文字起始位对齐。
- **权重感知 (Weight/Color Simulation)**：通过粗体、代码块模拟“颜色家族”和“视觉权重”。
- **结构化逻辑 (Structured Logic)**：模块化呈现，结论先行，脱水处理。

---

## 2. Telegram/文本规范 (Telegram/Text Protocol)

### 2.1 结构模板
1. **开篇**：报时 + 当前状态（1句）。
2. **业务块**：2-3个模块，使用 `**Emoji 标题 ｜ 副标题**`。
3. **列表层级**：
   - 一级：`• **字段** — 内容`
   - 二级：`  · 补充内容` (前面固定两个半角空格，使 `·` 与上方文字对齐)。
4. **重点**：核心结论或风险点**整句加粗**。
5. **技术项**：命令、端口、模型名使用 `代码块`。
6. **结尾**：`一句话总结：**结论。**` + `— 星宝 (模型名)`

---

## 3. 邮件专业规范 (Professional Email Protocol)

### 3.1 基础设置
- **发送者名称**：必须设为 `星宝` (使用 `formataddr` 协议)。
- **邮件标题**：格式为 `星宝执行报告 ｜ YYYY-MM-DD HH:MM`。
- **目标邮箱**：`hello.duan@foxmail.com`。

### 3.2 HTML/CSS 视觉架构 (移动端优化)
- **容器**：`max-width: 500px` (适配手机屏幕)，居中。
- **配色**：
  - 背景：`#f4f7f9` (浅灰蓝底)
  - 容器：`#ffffff` (纯白卡片)
  - 标题栏：`#1a1a1a` (深色/专业感)
- **排版**：
  - 模块标题：`font-size: 11px`, `uppercase`, `letter-spacing: 1px`, 带下划线。
  - 列表项：`margin-bottom: 15px`, 标签(Label)使用 `font-size: 11px`, `bold`。
  - 重点句：`font-size: 14px`, `color: #000`, `font-weight: 600`。
  - 总结区：`background: #f8f9fa`, `border-left: 4px solid #1a1a1a`。

### 3.3 邮件发送逻辑模板 (Python)
```python
from email.utils import formataddr
# ...
display_name = '星宝'
from_email = 'hello.junjie.duan@gmail.com'
msg['From'] = formataddr((display_name, from_email))
msg['Subject'] = f"星宝执行报告 ｜ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
```

---

## 4. 强制约束 (Hard Constraints)
- **禁止**：使用多层级编号 (1.1.1)、Markdown表格、花哨背景色、口水话。
- **必须**：在任何模型接手会话时，第一时间读取此文件并严格执行。
- **署名**：所有正式回复末尾必须署名 `— 星宝 (模型名)`。
