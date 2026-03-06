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
        
        # Search last 14 days for broader coverage
        date = (datetime.date.today() - datetime.timedelta(days=14)).strftime("%d-%b-%Y")
        print(f"Searching {username} since {date} for {keywords}...")
        
        results = []
        status, messages = mail.search(None, 'ALL')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            # Get last 50 emails to check for any missed ones
            recent_ids = msg_ids[-50:]
            for m_id in reversed(recent_ids):
                status, msg_data = mail.fetch(m_id, "(RFC822.HEADER)")
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
                        
                        found = False
                        for kw in keywords:
                            if kw.lower() in subject.lower() or kw.lower() in from_.lower():
                                found = True
                                break
                        
                        if found:
                            results.append(f"[{date_}] From: {from_} | Subject: {subject}")
        
        mail.logout()
        return results
    except Exception as e:
        return [f"Error checking {username}: {e}"]

if __name__ == "__main__":
    keywords = ["order", "bounty", "payment", "payout", "assigned", "claim", "upwork", "expensify", "tenstorrent", "hiring", "offer", "contract", "bounty-apply"]
    
    # Check Star Gmail (Star's "own" email)
    star_results = search_emails('imap.gmail.com', os.environ['GMAIL_STAR_USER'], os.environ['GMAIL_STAR_PASSWORD'], keywords)
    print("\n--- Star Gmail Results ---")
    for r in star_results: print(r)
    
    # Check Junjie Gmail
    gmail_results = search_emails('imap.gmail.com', os.environ['GMAIL_JUNJIE_USER'], os.environ['GMAIL_JUNJIE_PASSWORD'], keywords)
    print("\n--- Junjie Gmail Results ---")
    for r in gmail_results: print(r)
