# TOOLS.md - Available Tools

**Use tools directly. Never say "I can't" when a tool exists for it.**

## AI Search (Tavily & Serper)
- **Tavily**: `/Users/genesis/.openclaw/workspace-investor/tavily_search.sh "query"` (Best for AI-optimized content)
- **Serper**: `/Users/genesis/.openclaw/workspace-investor/serper_search.sh "query"` (Best for raw Google Search results)

## Core Tools
- **web_fetch** — Read any public URL, extract text
- **web_search** — Search the web
- **message** — Send to OTHER channels/people (NOT current conversation; just output text to reply)
- **exec** — Run shell commands on this Mac mini (macOS 15, Apple Silicon)

## Quick Reference (via exec)

| Task | Command |
|------|---------|
| Weather | `curl -s "wttr.in/萧山?format=3"` |
| A股行情 | `curl -s "https://hq.sinajs.cn/list=sh600519" \| iconv -f GBK -t UTF-8` |
| Translation | `trans :zh "text"` or `trans :en "中文"` |
| Screenshot | `screencapture -x ~/Desktop/screenshot.png` |
| TTS | `say -v Ting-Ting "你好"` |
| File search | `rg "pattern" /path` or `fd "name" /path` |

## Document Generation (Python via exec)
- PPT: `python-pptx` | Excel: `openpyxl` | PDF: `fpdf2` | Charts: `matplotlib`
- Calendar/Reminders: `osascript` (AppleScript)
- Video/Audio: `ffmpeg`, `yt-dlp`
- QR: `qrencode`

## Environment
- Mac mini (Apple Silicon), macOS 15, 杭州/萧山, Asia/Shanghai (GMT+8)
- Channels: iMessage, WhatsApp, Telegram
- Phone: +13433686913 | Email: hello.junjie.duan@gmail.com

## Rules
1. **Search first, ask never.** Always use tools before saying you can't.
2. **One reply only.** Output text directly. Do NOT also call `message` tool (= duplicate).
3. **Match user's language.** Chinese → Chinese. English → English.
4. **Be direct.** Do it, don't offer to do it.
