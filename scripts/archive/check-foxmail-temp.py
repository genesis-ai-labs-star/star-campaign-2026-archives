import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def check_unread():
    username = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    imap_url = 'imap.qq.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        # Search for all messages from today
        date = datetime.date.today().strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE {date})')
        
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} messages from today.")
            for m_id in msg_ids:
                status, msg_data = mail.fetch(m_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg.get('Subject'))[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')
                        from_ = msg.get('From')
                        print(f"\n--- Message {m_id.decode()} ---")
                        print(f"From: {from_}")
                        print(f"Subject: {subject}")
                        
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    print(f"Body:\n{body[:500]}...")
                                    break
                        else:
                            print(f"Body:\n{msg.get_payload(decode=True).decode()[:500]}...")
        else:
            print("No messages from today.")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_unread()
