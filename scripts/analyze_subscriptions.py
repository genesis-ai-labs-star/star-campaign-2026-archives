import imaplib
import email
import re
from datetime import datetime, timedelta

def analyze_emails(user, password, imap_url):
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select("inbox")
        
        # Search for common subscription keywords in the last 60 days
        date = (datetime.now() - timedelta(days=60)).strftime("%d-%b-%Y")
        search_query = f'(OR OR OR OR SUBJECT "subscription" SUBJECT "receipt" SUBJECT "bill" SUBJECT "invoice" SUBJECT "payment" SINCE {date})'
        
        result, data = mail.search(None, search_query)
        ids = data[0].split()
        
        subscriptions = []
        for i in ids[-50:]:  # Last 50 relevant emails to avoid timeout
            res, msg_data = mail.fetch(i, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    sender = msg["from"]
                    
                    # Basic extraction logic
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors='ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors='ignore')
                    
                    # Look for amounts (e.g., $9.99, 19.99 CAD)
                    amount_match = re.search(r'([\$£€]|CAD|USD)\s?(\d+\.\d{2})', body)
                    amount = amount_match.group(0) if amount_match else "Unknown"
                    
                    subscriptions.append({
                        "sender": sender,
                        "subject": subject,
                        "amount": amount,
                        "date": msg["date"]
                    })
        
        mail.logout()
        return subscriptions
    except Exception as e:
        return [f"Error analyzing {user}: {str(e)}"]

print("--- Gmail Analysis ---")
gmail_subs = analyze_emails("hello.junjie.duan@gmail.com", "msdb rmss jbuh rekx", "imap.gmail.com")
for s in gmail_subs:
    print(s)

print("\n--- Foxmail Analysis ---")
foxmail_subs = analyze_emails("hello.duan@foxmail.com", "awjyzuvhxdycjehb", "imap.qq.com")
for s in foxmail_subs:
    print(s)
