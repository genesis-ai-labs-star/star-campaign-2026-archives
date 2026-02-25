import imaplib

def try_login(u, p):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(u, p)
        print(f"SUCCESS: {u}")
        mail.logout()
    except Exception as e:
        print(f"FAILED: {u} - {e}")

try_login('genesis.ai.labs.star@gmail.com', 'YuLi@2026')
try_login('genesis.ai.labs.star@gmail.com', 'msdbrmssjbuhrekx')
