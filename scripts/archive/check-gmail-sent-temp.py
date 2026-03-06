import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_gmail_sent():
    username = os.environ['GMAIL_JUNJIE_USER']
    # Try both passwords
    passwords = [os.environ.get('GMAIL_JUNJIE_ALT_PASSWORD'), os.environ.get('GMAIL_JUNJIE_PASSWORD')]
    imap_url = 'imap.gmail.com'

    for password in passwords:
        if not password: continue
        try:
            print(f"Trying Gmail with password starting with {password[:3]}...")
            mail = imaplib.IMAP4_SSL(imap_url)
            mail.login(username, password)
            
            # Find Sent folder
            status, mailboxes = mail.list()
            sent_folder = '"[Gmail]/Sent Mail"'
            
            print(f"Selecting {sent_folder}...")
            mail.select(sent_folder)
            
            status, messages = mail.search(None, 'ALL')
            if status == 'OK' and messages[0]:
                msg_ids = messages[0].split()
                recent_ids = msg_ids[-20:]
                print(f"Timestamps of last {len(recent_ids)} sent Gmail emails:")
                for m_id in reversed(recent_ids):
                    status, msg_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (DATE SUBJECT TO)])")
                    header = msg_data[0][1].decode()
                    print(f"ID {m_id.decode()}: {header.strip().replace('\n', ' ')}")
            mail.logout()
            return
        except Exception as e:
            print(f"Error with this password: {e}")

if __name__ == "__main__":
    check_gmail_sent()
