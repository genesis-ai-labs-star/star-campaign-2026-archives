import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header, make_header
from datetime import datetime, timedelta
import collections

def safe_decode(header_value):
    if not header_value: return ""
    try: return str(make_header(decode_header(header_value)))
    except: return str(header_value)

def monitor_life_emails():
    username = os.environ['GMAIL_JUNJIE_USER']
    password = os.environ['GMAIL_JUNJIE_PASSWORD']
    imap_url = 'imap.gmail.com'
    
    # Check last 4 hours for any life-related updates
    since_time = (datetime.now() - timedelta(hours=4)).strftime("%d-%b-%Y")
    
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('"[Gmail]/All Mail"')
        
        # Search for logistics, bills, and health keywords
        keywords = ['amazon', 'fedex', 'ups', 'dhl', 'tracking', 'delivery', 'bill', 'invoice', 'payment', 'appointment', 'doctor', 'health', 'cra', 'tax']
        search_query = 'OR ' * (len(keywords) - 1) + ' '.join([f'SUBJECT "{k}"' for k in keywords])
        # Add SINCE to narrow down
        final_query = f'({search_query}) SINCE {since_time}'
        
        status, messages = mail.search(None, final_query)
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} potential life-ops updates in the last 4 hours.")
            for m_id in msg_ids:
                status, msg_data = mail.fetch(m_id, "(RFC822.HEADER)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        sender = safe_decode(msg.get('From', ''))
                        subject = safe_decode(msg.get('Subject', ''))
                        print(f"• [{sender}] {subject}")
        else:
            print("No new life-ops updates found in the last 4 hours.")
        mail.logout()
    except Exception as e:
        print(f"Life-Ops Watchdog Error: {e}")

if __name__ == "__main__":
    monitor_life_emails()
