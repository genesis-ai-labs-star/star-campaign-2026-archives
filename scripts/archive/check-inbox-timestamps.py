import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_inbox_timestamps():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('INBOX')
        
        status, messages = mail.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            recent_ids = msg_ids[-30:] 
            print(f"Timestamps of last {len(recent_ids)} inbox emails:")
            for m_id in reversed(recent_ids):
                status, msg_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (DATE SUBJECT)])")
                header = msg_data[0][1].decode()
                print(f"ID {m_id.decode()}: {header.strip().replace('\n', ' ')}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_inbox_timestamps()
