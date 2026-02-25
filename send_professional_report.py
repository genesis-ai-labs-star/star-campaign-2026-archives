import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_email(subject, html_content, to_email):
    from_email = "hello.duan@foxmail.com"
    password = "awjyzuvhxdycjehb"
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    subject = sys.argv[1]
    to_addr = sys.argv[2]
    html = sys.stdin.read()
    if send_email(subject, html, to_addr):
        print("Success")
    else:
        sys.exit(1)
