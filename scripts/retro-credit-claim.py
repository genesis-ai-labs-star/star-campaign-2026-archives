import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

def send_claim_email():
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    to_email = 'ffp@airchina.com'
    cc_email = 'hello.duan@foxmail.com'
    display_name = '星宝'
    
    card_number = '052006142129'
    user_name = 'DUAN JUNJIE'
    
    subject = f"【里程补登申请】星空联盟金卡会员 - {user_name} - {card_number}"
    
    body = f"""尊敬的国航凤凰知音客服：

您好！

我是凤凰知音金卡会员 {user_name}（卡号：{card_number}）。

由于国航 App 的“合作伙伴补登”页面无法正常录入加航（Air Canada）及国泰航空（Cathay Pacific）的票号（系统提示票号长度或格式不支持），现通过邮件申请人工补登以下航段的里程及航段。

以下是我的近期飞行明细：

1. 2026-02-22 | 航班号：AC458 | 票号：0142321144162 | 航段：多伦多(YYZ) -> 渥太华(YOW)
2. 2026-02-22 | 航班号：AC472 | 票号：0142321099351 | 航段：多伦多(YYZ) -> 渥太华(YOW)
3. 2026-02-19 | 航班号：AC447 | 票号：0142320930280 | 航段：渥太华(YOW) -> 多伦多(YYZ)
4. 2026-02-11 | 航班号：AC472 | 票号：0142320179717 | 航段：多伦多(YYZ) -> 渥太华(YOW)
5. 2026-01-28 | 航班号：CX805 | 票号：1606396429991 | 航段：多伦多(YYZ) -> 香港(HKG)
6. 2026-01-13 | 航班号：AC467 | 票号：0142317691751 | 航段：渥太华(YOW) -> 多伦多(YYZ)

以上行程单均可在我的预留邮箱中查实。如果需要进一步的登机牌扫描件，请随时告知。

感谢您的协助，祝工作顺利！

---
凤凰知音金卡会员：{user_name}
会员卡号：{card_number}
发送日期：{datetime.now().strftime('%Y-%m-%d')}
"""

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    msg['Cc'] = cc_email
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
        server.login(from_email, password)
        recipients = [to_email, cc_email]
        server.sendmail(from_email, recipients, msg.as_string())
        server.quit()
        print("SUCCESS: Claim email sent to ffp@airchina.com and CCed to you.")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    send_claim_email()
