import imaplib
import email
from email.header import decode_header

def check_upwork_email():
    username = 'hello.junjie.duan@gmail.com'
    password = 'msdbrmssjbuhrekx'
    imap_url = 'imap.gmail.com'

    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('"[Gmail]/All Mail"')
        
        # Broad search
        status, messages = mail.search(None, '(OR FROM "Upwork" SUBJECT "Upwork")')
        if status == 'OK' and messages[0]:
            msg_ids = messages[0].split()
            print(f"Found {len(msg_ids)} matches.")
            for m_id in msg_ids[-5:]:
                status, msg_data = mail.fetch(m_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        print(f"Date: {msg.get('Date')} | From: {msg.get('From')} | Subject: {msg.get('Subject')}")
        else:
            print("No matches for 'Upwork' in From or Subject.")
        
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_upwork_email()
