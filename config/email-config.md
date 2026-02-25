# 邮件配置

## Gmail
- 账号：hello.junjie.duan@gmail.com
- App Password：msdb rmss jbuh rekx
- SMTP：smtp.gmail.com:587 (TLS)
- IMAP：imap.gmail.com:993

## Foxmail / QQ邮箱
- 账号：hello.duan@foxmail.com
- 授权码：awjyzuvhxdycjehb
- SMTP：smtp.qq.com:587
- IMAP：imap.qq.com:993

## 发邮件示例（Python）
```python
import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body, account='gmail'):
    if account == 'gmail':
        sender = 'hello.junjie.duan@gmail.com'
        password = 'msdbrmssjbuhrekx'
        smtp_host = 'smtp.gmail.com'
    else:  # foxmail
        sender = 'hello.duan@foxmail.com'
        password = 'awjyzuvhxdycjehb'
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

_更新于 2026-02-18_
