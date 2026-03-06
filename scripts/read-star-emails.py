import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def read_recent_star_emails():
    username = os.environ['GMAIL_STAR_USER']
    password = os.environ['GMAIL_STAR_PASSWORD']
    imap_url = 'imap.gmail.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        status, messages = mail.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            # Check last 10 emails
            recent_ids = msg_ids[-10:]
            print(f"Reading last {len(recent_ids)} messages from Star account.")
            for m_id in reversed(recent_ids):
                status, msg_data = mail.fetch(m_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = ""
                        decoded_subject = decode_header(msg.get('Subject', ''))[0]
                        if isinstance(decoded_subject[0], bytes):
                            subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
                        else:
                            subject = decoded_subject[0]
                        
                        from_ = msg.get('From')
                        date_ = msg.get('Date')
                        print(f"\n--- Message {m_id.decode()} ---")
                        print(f"From: {from_}")
                        print(f"Subject: {subject}")
                        print(f"Date: {date_}")
                        
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    try:
                                        body = part.get_payload(decode=True).decode()
                                        break
                                    except:
                                        pass
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode()
                            except:
                                pass
                        print(f"Body:\n{body[:2000]}...")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_recent_star_emails()
