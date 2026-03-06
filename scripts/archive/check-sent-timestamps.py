import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_sent_timestamps():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        
        # List mailboxes to find "Sent"
        status, mailboxes = mail.list()
        for mb in mailboxes:
            print(f"Mailbox: {mb.decode()}")
        
        sent_folder = "Sent Messages"
        for mb in mailboxes:
            mb_str = mb.decode()
            if "Sent" in mb_str or "已发送" in mb_str:
                parts = mb_str.split('"')
                sent_folder = parts[-2]
                break
        
        print(f"Selecting {sent_folder}...")
        mail.select(sent_folder)
        
        status, messages = mail.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            recent_ids = msg_ids[-20:] # Last 20
            print(f"Timestamps of last {len(recent_ids)} sent emails:")
            for m_id in reversed(recent_ids):
                status, msg_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (DATE SUBJECT)])")
                header = msg_data[0][1].decode()
                print(f"ID {m_id.decode()}: {header.strip().replace('\n', ' ')}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_sent_timestamps()
