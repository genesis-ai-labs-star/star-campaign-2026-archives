import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_foxmail_today():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('INBOX')
        
        # Search for messages since today (March 2nd, 2026)
        # Note: IMAP SINCE is "messages whose internal date is since the specified date"
        status, messages = mail.search(None, '(SINCE 02-Mar-2026)')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} messages in Foxmail inbox since today.")
            
            # Print last 10 subjects and froms
            for m_id in msg_ids[-10:]:
                status, msg_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (DATE SUBJECT FROM)])")
                header = msg_data[0][1].decode()
                print(f"ID {m_id.decode()}: {header.strip().replace('\n', ' ')}")
        else:
            print("No messages found since today.")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_foxmail_today()
