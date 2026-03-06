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
    
    subject = f"【里程补登申请-补充清单】星空联盟金卡会员 - {user_name} - {card_number}"
    
    body = f"""尊敬的国航凤凰知音客服：

您好！

我是凤凰知音金卡会员 {user_name}（卡号：{card_number}）。

接上一封邮件，我整理了过去半年内（2025年10月至今）所有未成功累积的加航（Air Canada）及国泰航空（Cathay Pacific）航段，请一并予以补登。

以下是完整的待处理清单（含上一封邮件内容）：

1. 2025-10-14 | 航班：AC469/CX829 | 票号：1602787082872
2. 2025-10-23 | 航班：AC345 | 票号：0142750950292
3. 2025-10-26 | 航班：AC342 | 票号：0142750951643
4. 2025-11-11 | 航班：AC345 | 票号：0142754489626
5. 2025-11-14 | 航班：AC346 | 票号：0146046470024
6. 2025-12-07 | 航班：AC447 | 票号：0145089397039
7. 2025-12-09 | 航班：AC458 | 票号：0145089397349
8. 2025-12-13 | 航班：AC463 | 票号：0145089398794
9. 2025-12-19 | 航班：AC466 | 票号：0145089400055
10. 2025-12-19 | 航班：AC458 | 票号：0145089400081
11. 2026-01-13 | 航班：AC467 | 票号：0142317691751
12. 2026-01-28 | 航班：AC447/CX805 | 票号：1606396429991
13. 2026-01-28 | 航班：AC465/CX829 | 票号：1602129101498
14. 2026-02-10 | 航班：CX826/CX959 | 票号：1605508549606
15. 2026-02-11 | 航班：AC472 | 票号：0142320179717
16. 2026-02-19 | 航班：AC447 | 票号：0142320930280
17. 2026-02-22 | 航班：AC472 | 票号：0142321099351
18. 2026-02-22 | 航班：AC458 | 票号：0142321144162

以上所有行程均已核实，请协助处理里程及航段累积，以确保我的金卡会籍正常延续。

感谢！

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
        print("SUCCESS: Comprehensive claim email sent.")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    send_claim_email()
