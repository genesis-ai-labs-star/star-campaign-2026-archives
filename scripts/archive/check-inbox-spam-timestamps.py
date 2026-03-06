import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_inbox_spam_timestamps():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('INBOX')
        
        # Check IDs 5990 to 6009
        for m_id in range(5990, 6010):
            status, msg_data = mail.fetch(str(m_id), "(BODY[HEADER.FIELDS (DATE SUBJECT FROM)])")
            if status == 'OK' and msg_data[0]:
                header = msg_data[0][1].decode()
                print(f"ID {m_id}: {header.strip().replace('\n', ' ')}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_inbox_spam_timestamps()
