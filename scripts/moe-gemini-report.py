import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import google.generativeai as genai
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def generate_moe_diagram_and_report():
    # Use the latest model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = """
    你是一个顶级的 AI 架构师。请为段俊杰（老段）生成一份关于 MoE (Mixture of Experts) 物理架构的深度技术分析报告。
    
    要求：
    1. 语言：中文。
    2. 包含一个精美的、结构化的 ASCII 或文本图表，展示：
       - 专家（Experts）在 GPU HBM 显存中的物理分布。
       - Token 路由（Router）与 All-to-All 通信的逻辑流向。
       - 高维向量空间的语义分区概念。
    3. 风格：商务简约、仪表盘风格。
    4. 结尾署名：— 星宝 (Gemini 2.0 Flash 增强版)。
    
    输出格式：直接输出 HTML 代码，用于发送邮件。使用内联 CSS 确保移动端适配良好。
    """
    
    response = model.generate_content(prompt)
    report_html = response.text
    
    # Cleaning markdown if Gemini wrapped it
    if "```html" in report_html:
        report_html = report_html.split("```html")[1].split("```")[0]
    elif "<html>" not in report_html:
        # Fallback to wrapping it if it's just raw text/markdown
        report_html = f"<html><body style='font-family:sans-serif; padding:20px;'>{report_html}</body></html>"
    
    send_to_user(report_html)

def send_to_user(html_content):
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    to_email = 'hello.duan@foxmail.com'
    display_name = '星宝'
    
    msg = MIMEMultipart()
    msg['Subject'] = f"Gemini 增强版：MoE 物理深度架构报告 ｜ {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Gemini enhanced report sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    generate_moe_diagram_and_report()
