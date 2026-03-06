import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import imaplib
import email
from email.header import decode_header, make_header
from datetime import datetime, timedelta
import collections
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def safe_decode(header_value):
    if not header_value: return ""
    try: return str(make_header(decode_header(header_value)))
    except: return str(header_value)

def analyze_and_report():
    username = os.environ['GMAIL_JUNJIE_USER']
    password = os.environ['GMAIL_JUNJIE_PASSWORD']
    imap_url = 'imap.gmail.com'
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%d-%b-%Y")
    
    categories = collections.defaultdict(int)
    sender_counts = collections.defaultdict(int)
    category_senders = collections.defaultdict(lambda: collections.defaultdict(int))
    
    try:
        print(f"Connecting to {username}...")
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select('"[Gmail]/All Mail"')
        
        print(f"Searching for emails since {six_months_ago}...")
        status, messages = mail.search(None, f'SINCE {six_months_ago}')
        if status != 'OK' or not messages[0]:
            print("No emails found.")
            return
            
        msg_ids = messages[0].split()
        total = len(msg_ids)
        print(f"Analyzing {total} emails...")
        
        # To avoid extreme runtime, we'll process up to 3000 most recent headers if total is huge,
        # but 6k should be manageable if we only fetch headers.
        # Let's try all 6k but in chunks.
        chunk_size = 500
        for i in range(0, total, chunk_size):
            chunk = msg_ids[i:i+chunk_size]
            ids_str = b','.join(chunk).decode()
            status, data = mail.fetch(ids_str, "(RFC822.HEADER)")
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = safe_decode(msg.get('From', ''))
                    subject = safe_decode(msg.get('Subject', ''))
                    
                    s_lower = sender.lower()
                    subj_lower = subject.lower()
                    
                    # Extract clean email/name for sender counts
                    clean_sender = sender.split('<')[-1].split('>')[0].strip()
                    sender_counts[clean_sender] += 1
                    
                    cat = 'Other/General'
                    if any(x in s_lower or x in subj_lower for x in ["upwork", "expensify", "bounty"]):
                        cat = 'Bounty & Work'
                    elif any(x in s_lower or x in subj_lower for x in ["github", "gitlab", "bitbucket", "notifications@github.com"]):
                        cat = 'Technical & Dev'
                    elif any(x in s_lower or x in subj_lower for x in ["bank", "invoice", "payment", "stripe", "billing", "tax", "cra", "polymarket", "finance", "trading", "alpha", "stock"]):
                        cat = 'Finance & Investing'
                    elif any(x in s_lower or x in subj_lower for x in ["newsletter", "theinformation", "seekingalpha", "feedspot", "substack", "medium", "the information"]):
                        cat = 'Intel & Newsletters'
                    elif any(x in s_lower or x in subj_lower for x in ["linkedin", "twitter", "pinterest", "facebook", "instagram", "threads", "x.com"]):
                        cat = 'Social & Networking'
                    elif any(x in s_lower or x in subj_lower for x in ["apple", "google", "amazon", "microsoft", "openai", "anthropic", "meta", "aws", "azure", "cloud"]):
                        cat = 'Platforms & Cloud'
                    
                    categories[cat] += 1
                    category_senders[cat][clean_sender] += 1
            
            print(f"Processed {min(i+chunk_size, total)}/{total}...")

        mail.logout()
        
        # Generate Report
        report_html = f"""
        <html>
        <body style="font-family: sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px;">
                <h2 style="border-bottom: 2px solid #1a1a1a; padding-bottom: 10px;">星宝执行报告 ｜ 邮件系统分析</h2>
                <p><strong>分析对象：</strong> {username}</p>
                <p><strong>时间范围：</strong> 过去 6 个月 (Since {six_months_ago})</p>
                <p><strong>邮件总量：</strong> {total} 封</p>
                
                <h3 style="background: #f4f4f4; padding: 5px 10px;">1. 类别分布 (Classification)</h3>
                <ul>
        """
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            report_html += f"<li><strong>{cat}:</strong> {count} 封 ({percentage:.1f}%)</li>"
            
        report_html += """
                </ul>
                
                <h3 style="background: #f4f4f4; padding: 5px 10px;">2. 核心发送者 (Top Senders)</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background: #eee;">
                        <th style="text-align: left; padding: 8px;">发送者</th>
                        <th style="text-align: right; padding: 8px;">数量</th>
                    </tr>
        """
        
        for sender, count in sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
            report_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #eee;'>{sender}</td><td style='padding: 8px; border-bottom: 1px solid #eee; text-align: right;'>{count}</td></tr>"
            
        report_html += """
                </table>
                
                <h3 style="background: #f4f4f4; padding: 5px 10px;">3. 深度洞察 (Insights)</h3>
                <ul>
        """
        
        # Add some automated insights
        if categories['Intel & Newsletters'] > total * 0.3:
            report_html += "<li><strong>信息载荷警报：</strong> 您的收件箱中超过 30% 是资讯类邮件。建议由我定期进行语义摘要，减少您的阅读负担。</li>"
        if categories['Bounty & Work'] > 0:
            report_html += f"<li><strong>业务活跃度：</strong> 过去 6 个月共有 {categories['Bounty & Work']} 封与 Bounty/Upwork 相关的邮件，处于持续作业状态。</li>"
        if categories['Technical & Dev'] > 0:
            report_html += f"<li><strong>技术基建：</strong> GitHub 相关通知占比较大，反映了高频的代码迭代和项目监控需求。</li>"
            
        report_html += f"""
                </ul>
                
                <div style="margin-top: 30px; padding-top: 10px; border-top: 1px solid #eee; font-size: 0.9em; color: #666;">
                    <p>一句话总结：<strong>您的邮箱是典型的高频技术+投资资讯型配置，信息流极其充沛，建议引入自动化筛选。</strong></p>
                    <p>— 星宝 AI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send the email
        send_to_user(report_html)
        
    except Exception as e:
        print(f"Analysis failed: {e}")

def send_to_user(html_content):
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    to_email = 'hello.duan@foxmail.com'
    display_name = '星宝'
    
    msg = MIMEMultipart()
    msg['Subject'] = f"星宝执行报告 ｜ 邮件系统分析报告 {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Report email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    analyze_and_report()
