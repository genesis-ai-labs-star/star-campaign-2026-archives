import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

def send_visual_report():
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    to_email = 'hello.duan@foxmail.com'
    display_name = '星宝'
    
    msg = MIMEMultipart()
    msg['Subject'] = f"视觉增强版报告：MoE 物理架构与数据流向图解 ｜ {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    
    html_content = f"""
    <html>
    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1a1a1a; line-height: 1.6; background-color: #f4f7f9; margin: 0; padding: 20px;">
        <div style="max-width: 700px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #e1e1e1;">
            
            <!-- Header -->
            <div style="border-bottom: 3px solid #1a1a1a; padding-bottom: 20px; margin-bottom: 30px; text-align: center;">
                <h1 style="font-size: 28px; margin: 0; letter-spacing: 2px; color: #000; font-weight: 800;">视觉技术看板</h1>
                <p style="font-size: 14px; color: #666; text-transform: uppercase; margin-top: 10px; letter-spacing: 1px;">Visualizing MoE & Compute Network Architecture</p>
            </div>

            <!-- Section 1: Physical Structure -->
            <div style="margin-bottom: 45px;">
                <h3 style="font-size: 16px; text-transform: uppercase; letter-spacing: 1.5px; color: #d32f2f; background: #ffebee; padding: 8px 15px; border-radius: 4px; margin-bottom: 20px;">01. MoE 专家实体的物理拓扑</h3>
                <p style="font-size: 15px; margin-bottom: 15px;">在物理显存中，专家不是虚无的逻辑，而是<strong>分块存储的 MLP 权重矩阵</strong>：</p>
                <div style="text-align: center; background: #fafafa; padding: 20px; border: 1px dashed #ccc; border-radius: 8px; margin-bottom: 15px;">
                    <code style="font-size: 13px; color: #555; line-height: 1.2; display: block; text-align: left;">
                    [ GPU HBM Address Space ]<br>
                    |--- Attention Layers (Shared) ---|<br>
                    |--- Router (Gate Network)     ---|<br>
                    |--- Expert 01 (MLP Weights)   ---|<br>
                    |--- Expert 02 (MLP Weights)   ---|<br>
                    |--- ...                       ---|<br>
                    |--- Expert 64 (MLP Weights)   ---|<br>
                    </code>
                </div>
                <p style="font-size: 14px; color: #666;"><strong>视觉洞察：</strong> 显存就像一个巨大的货架，路由是管理员，根据 Token 的“提货单”瞬间定位到对应的专家矩阵进行计算。</p>
            </div>

            <!-- Section 2: Data Flow (All-to-All) -->
            <div style="margin-bottom: 45px;">
                <h3 style="font-size: 16px; text-transform: uppercase; letter-spacing: 1.5px; color: #1976d2; background: #e3f2fd; padding: 8px 15px; border-radius: 4px; margin-bottom: 20px;">02. All-to-All 数据流向图解</h3>
                <p style="font-size: 15px; margin-bottom: 15px;">当 Token 在不同显卡上的专家间跳转时，算力网络承受的是<strong>非均匀、高频的分拣压力</strong>：</p>
                <div style="text-align: center; background: #1a1a1a; padding: 30px; border-radius: 8px; margin-bottom: 15px; color: #00ff00; font-family: monospace;">
                    <pre style="margin: 0; font-size: 12px;">
    [GPU 0] --(Token A: 8KB)--> [Router] --\
                                            \--> [Switch] --\
    [GPU 1] --(Token B: 8KB)--> [Router] --/             \--> [GPU N (Expert 5)]
                                                         \--> [GPU M (Expert 8)]
                    </pre>
                </div>
                <p style="font-size: 14px; color: #666;"><strong>视觉洞察：</strong> 这不是传统的“广播”或“同步”，而是类似于<strong>全球快递分拣中心</strong>。每个 Token 包（8KB）都有明确的目的地，网络必须支持极高的对分带宽以防“爆仓”。</p>
            </div>

            <!-- Section 3: Vector Space -->
            <div style="margin-bottom: 45px;">
                <h3 style="font-size: 16px; text-transform: uppercase; letter-spacing: 1.5px; color: #388e3c; background: #e8f5e9; padding: 8px 15px; border-radius: 4px; margin-bottom: 20px;">03. 向量空间的“经纬度”</h3>
                <p style="font-size: 15px; margin-bottom: 15px;">向量表征能力来自于<strong>高维空间的唯一性定位</strong>：</p>
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="display: inline-block; width: 100px; height: 100px; border: 2px solid #388e3c; border-radius: 50%; position: relative;">
                        <div style="position: absolute; top: 20%; left: 30%; width: 6px; height: 6px; background: red; border-radius: 50%;"></div>
                        <div style="position: absolute; top: 25%; left: 35%; width: 6px; height: 6px; background: red; border-radius: 50%;"></div>
                        <div style="position: absolute; bottom: 20%; right: 30%; width: 6px; height: 6px; background: blue; border-radius: 50%;"></div>
                        <span style="position: absolute; top: 10%; left: 40%; font-size: 10px;">"Cat/Dog"</span>
                        <span style="position: absolute; bottom: 10%; right: 40%; font-size: 10px;">"CPU/GPU"</span>
                    </div>
                </div>
                <p style="font-size: 14px; color: #666;"><strong>视觉洞察：</strong> 4096 维空间被切分为无数个“语义教区”。MoE 专家负责看管特定的教区。当一个坐标点落下，对应的专家就会被瞬间唤醒。</p>
            </div>

            <!-- Summary -->
            <div style="background-color: #333; color: #fff; padding: 25px; border-radius: 8px;">
                <p style="font-size: 16px; font-weight: 600; margin: 0; color: #00ff00;">司令官洞察：</p>
                <p style="font-size: 14px; margin-top: 10px;">MoE 的物理落地，标志着 AI 设施从<strong>“暴力计算”</strong>转向<strong>“精准调度”</strong>。未来的投资核心不在于谁能买到最多的卡，而在于谁能构建出最无损、最低延迟的<strong>算力神经连接网络</strong>。</p>
            </div>

            <!-- Footer -->
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: right;">
                <p style="font-size: 13px; color: #888; font-style: italic;">Visualized by 星宝 (Main Agent)</p>
                <p style="font-size: 12px; color: #aaa; margin-top: 5px;">星宝 AI</p>
            </div>

        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Visual technical report email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    send_visual_report()
