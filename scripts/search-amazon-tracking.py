import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def search_amazon():
    username = os.environ['GMAIL_JUNJIE_USER']
    password = os.environ['GMAIL_JUNJIE_ALT_PASSWORD']
    imap_url = 'imap.gmail.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        date = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE {date} FROM "Amazon.ca")')
        
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} Amazon messages.")
            for m_id in msg_ids[-3:]: # Get the last 3
                status, msg_data = mail.fetch(m_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg.get('Subject'))[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')
                        print(f"Subject: {subject}")
                        # Extract body to find tracking or delivery date
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    print(f"Body snippet: {body[:500]}...")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()
                            print(f"Body snippet: {body[:500]}...")
        else:
            print("No Amazon messages found since " + date)
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_amazon()
