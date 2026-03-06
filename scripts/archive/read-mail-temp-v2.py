import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def read_msg(m_id):
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        status, msg_data = mail.fetch(str(m_id), "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                from_ = msg.get('From')
                subject = decode_header(msg.get('Subject'))[0]
                if isinstance(subject[0], bytes):
                    subject = subject[0].decode(subject[1] or 'utf-8')
                else:
                    subject = subject[0]
                print(f"From: {from_}")
                print(f"Subject: {subject}")
                
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        print(f"Part: {content_type}")
                        if content_type == "text/plain" or content_type == "text/html":
                            try:
                                payload = part.get_payload(decode=True).decode()
                                print(f"Body ({content_type}):\n{payload[:1000]}")
                            except:
                                print(f"Could not decode {content_type}")
                else:
                    print(f"Body:\n{msg.get_payload(decode=True).decode()[:1000]}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    read_msg(sys.argv[1] if len(sys.argv) > 1 else 5990)
