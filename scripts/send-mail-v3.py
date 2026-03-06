import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import sys
from datetime import datetime

def send_mail(to_email, subject, body, file_path=None):
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    display_name = '星宝'
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    
    msg.attach(MIMEText(body, 'plain'))
    
    if file_path:
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
                msg.attach(part)
        except Exception as e:
            print(f"Attachment Error: {e}")

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_mail_v3.py <to> <subject> <body> [file_path]")
        sys.exit(1)
    
    target_to = sys.argv[1]
    target_subject = sys.argv[2]
    target_body = sys.argv[3]
    target_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    if send_mail(target_to, target_subject, target_body, target_file):
        print("Success")
    else:
        sys.exit(1)
