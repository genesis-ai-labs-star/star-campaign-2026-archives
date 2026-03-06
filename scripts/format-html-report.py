import sys
from datetime import datetime

def generate_html_report(content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 简单的 Markdown 转 HTML (针对本报告结构)
    html_body = content.replace("\n", "<br>")
    html_body = html_body.replace("### ", "<h3 style='margin-top:0; color:#1a1a1a;'>").replace("\n", "</h3>", 1)
    html_body = html_body.replace("**", "<b>").replace("**", "</b>")
    
    html = f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f7f9; padding: 20px;">
        <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #666; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px;">
                EVOLUTION DASHBOARD REPORT
            </div>
            <div style="line-height: 1.6; color: #333;">
                {html_body}
            </div>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #888; background-color: #f8f9fa; border-left: 4px solid #1a1a1a; padding-left: 15px;">
                此报告由星宝系统自动生成。
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # 从 stdin 读取 report text
    report_text = sys.stdin.read()
    print(generate_html_report(report_text))
