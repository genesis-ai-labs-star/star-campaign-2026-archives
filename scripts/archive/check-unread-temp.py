import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_unread():
    username = os.environ['GMAIL_JUNJIE_USER']
    password = os.environ['GMAIL_JUNJIE_ALT_PASSWORD']
    imap_url = 'imap.gmail.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        # Search for unread messages from the last 2 days
        date = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(UNSEEN SINCE {date})')
        
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} unread messages.")
            for m_id in msg_ids:
                status, msg_data = mail.fetch(m_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg.get('Subject'))[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')
                        from_ = msg.get('From')
                        print(f"- {from_}: {subject}")
        else:
            print("No unread messages.")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_unread()
