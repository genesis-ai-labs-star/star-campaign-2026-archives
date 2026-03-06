# 邮件配置

## Gmail
- 账号：见 `~/.openclaw/.env` → `GMAIL_JUNJIE_USER`
- App Password：见 `~/.openclaw/.env` → `GMAIL_JUNJIE_ALT_PASSWORD`
- SMTP：smtp.gmail.com:587 (TLS)
- IMAP：imap.gmail.com:993

## Foxmail / QQ邮箱
- 账号：见 `~/.openclaw/.env` → `FOXMAIL_USER`
- 授权码：见 `~/.openclaw/.env` → `FOXMAIL_PASSWORD`
- SMTP：smtp.qq.com:465 (SSL) / 587 (TLS)
- IMAP：imap.qq.com:993

## 发邮件示例（Python）
```python
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body, account='gmail'):
    if account == 'gmail':
        sender = os.environ['GMAIL_JUNJIE_USER']
        password = os.environ['GMAIL_JUNJIE_ALT_PASSWORD']
        smtp_host = 'smtp.gmail.com'
    else:  # foxmail
        sender = os.environ['FOXMAIL_USER']
        password = os.environ['FOXMAIL_PASSWORD']
        smtp_host = 'smtp.qq.com'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    with smtplib.SMTP(smtp_host, 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [to], msg.as_string())
```

_更新于 2026-03-02 — 凭据已迁移至 .env (GOVERNANCE 第九条)_
