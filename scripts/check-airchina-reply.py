import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_airchina_reply():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('INBOX')
        
        status, msg_data = mail.fetch('5990', "(RFC822)")
        if status == 'OK':
            msg = email.message_from_bytes(msg_data[0][1])
            print(f"From: {msg.get('From')}")
            print(f"Subject: {msg.get('Subject')}")
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    print(f"Part: {content_type}")
                    if "text" in content_type:
                        try:
                            text = part.get_payload(decode=True).decode('utf-8')
                        except:
                            text = part.get_payload(decode=True).decode('gbk', 'ignore')
                        print(f"Content: {text[:200]}")
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8')
                except:
                    body = msg.get_payload(decode=True).decode('gbk', 'ignore')
                print(f"Body: {body[:200]}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_airchina_reply()
