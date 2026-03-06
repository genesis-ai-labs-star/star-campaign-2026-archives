import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header
import datetime

def search_emails(imap_url, username, password, keywords):
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('inbox')
        
        # Search last 7 days
        date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%d-%b-%Y")
        print(f"Searching {username} since {date} for {keywords}...")
        
        results = []
        for keyword in keywords:
            status, messages = mail.search(None, f'(SINCE {date} SUBJECT "{keyword}")')
            if status == 'OK' and messages[0]:
                msg_ids = messages[0].split()
                for m_id in msg_ids:
                    status, msg_data = mail.fetch(m_id, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = decode_header(msg.get('Subject'))[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or 'utf-8')
                            from_ = msg.get('From')
                            date_ = msg.get('Date')
                            results.append(f"[{date_}] From: {from_} | Subject: {subject}")
        
        mail.logout()
        return results
    except Exception as e:
        return [f"Error checking {username}: {e}"]

if __name__ == "__main__":
    keywords = ["order", "bounty", "payment", "payout", "assigned", "claim", "upwork", "expensify", "tenstorrent"]
    
    # Check Foxmail
    fox_results = search_emails('imap.qq.com', os.environ['FOXMAIL_USER'], os.environ['FOXMAIL_PASSWORD'], keywords)
    print("\n--- Foxmail Results ---")
    for r in fox_results: print(r)
    
    # Check Gmail (using ALT_PASSWORD as the watchdog does)
    gmail_results = search_emails('imap.gmail.com', os.environ['GMAIL_JUNJIE_USER'], os.environ['GMAIL_JUNJIE_ALT_PASSWORD'], keywords)
    print("\n--- Gmail Results ---")
    for r in gmail_results: print(r)
