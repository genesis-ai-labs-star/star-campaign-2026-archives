import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_sent_folder():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        
        status, mailboxes = mail.list()
        # Find the one that is the sent folder
        sent_folder = None
        for mb in mailboxes:
            mb_str = mb.decode()
            if "Sent" in mb_str or "已发送" in mb_str:
                parts = mb_str.split('"')
                sent_folder = parts[-2]
                break
        
        if not sent_folder:
            print("Could not find sent folder.")
            return

        print(f"Selecting {sent_folder}...")
        # Use quotes for folder name
        mail.select(f'"{sent_folder}"')
        
        status, messages = mail.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            recent_ids = msg_ids[-100:] # Last 100
            print(f"Total sent: {len(msg_ids)}. Checking last {len(recent_ids)}.")
            
            subjects = collections.defaultdict(int)
            last_date = None
            
            for m_id in msg_ids[-50:]:
                status, msg_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (DATE SUBJECT)])")
                header = msg_data[0][1].decode()
                subject = "Unknown"
                date = "Unknown"
                for line in header.split('\n'):
                    if line.lower().startswith('subject:'):
                        subject = line[8:].strip()
                    if line.lower().startswith('date:'):
                        date = line[5:].strip()
                print(f"ID {m_id.decode()}: {date} | {subject}")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import collections
    check_sent_folder()
