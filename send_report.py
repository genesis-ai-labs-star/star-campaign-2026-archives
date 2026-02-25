import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_email(subject, body, to_email):
    # 根据 MEMORY.md 中的配置
    from_email = "hello.duan@foxmail.com"
    password = "awjyzuvhxdycjehb"
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    subj = sys.argv[1]
    content = sys.argv[2]
    target = sys.argv[3]
    if send_email(subj, content, target):
        print("Success")
    else:
        sys.exit(1)
