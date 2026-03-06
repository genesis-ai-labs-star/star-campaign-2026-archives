import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

def send_final_report():
    from_email = os.environ['FOXMAIL_USER']
    password = os.environ['FOXMAIL_PASSWORD']
    to_email = 'hello.duan@foxmail.com'
    display_name = '星宝'
    
    msg = MIMEMultipart()
    msg['Subject'] = f"终极视觉报告：MoE 物理全景架构图解 ｜ {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    
    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f0f2f5; margin: 0; padding: 20px;">
        <div style="max-width: 800px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #434343 100%); padding: 30px; border-radius: 10px; margin-bottom: 40px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 32px; letter-spacing: 2px;">MoE 物理架构全景报告</h1>
                <p style="margin-top: 10px; opacity: 0.8; font-size: 14px; text-transform: uppercase;">Physical Mapping & Data Flow Visualization</p>
            </div>

            <!-- Visualization 1: HBM Layout -->
            <div style="margin-bottom: 50px;">
                <h2 style="font-size: 18px; border-left: 5px solid #ff4b2b; padding-left: 15px; margin-bottom: 25px;">1. 显存物理布局 (HBM Memory Map)</h2>
                <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 25px; font-family: 'Courier New', Courier, monospace;">
                    <div style="border: 2px solid #333; padding: 15px;">
                        <div style="text-align: center; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold;">GPU HBM (High Bandwidth Memory)</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                            <div style="width: 140px; height: 60px; background: #e9ecef; border: 1px solid #adb5bd; display: flex; align-items: center; justify-content: center; font-size: 12px;">Shared Attention</div>
                            <div style="width: 140px; height: 60px; background: #e9ecef; border: 1px solid #adb5bd; display: flex; align-items: center; justify-content: center; font-size: 12px;">Router / Gate</div>
                            <div style="width: 140px; height: 60px; background: #ffcccc; border: 2px solid #ff4b2b; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold;">Expert 01 (MLP)</div>
                            <div style="width: 140px; height: 60px; background: #ffcccc; border: 2px solid #ff4b2b; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold;">Expert 02 (MLP)</div>
                            <div style="width: 140px; height: 60px; background: #ffcccc; border: 2px solid #ff4b2b; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold;">Expert 03 (MLP)</div>
                            <div style="width: 140px; height: 60px; background: #ffcccc; border: 2px solid #ff4b2b; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold;">Expert 04 (MLP)</div>
                        </div>
                    </div>
                </div>
                <p style="font-size: 14px; color: #666; margin-top: 15px;">专家在物理上是<strong>显存中的连续地址空间</strong>。MoE 推理时，计算核心根据路由指令，通过内存偏移量（Offset）精准抓取对应专家的权重数据。</p>
            </div>

            <!-- Visualization 2: All-to-All Flow -->
            <div style="margin-bottom: 50px;">
                <h2 style="font-size: 18px; border-left: 5px solid #007bff; padding-left: 15px; margin-bottom: 25px;">2. All-to-All 交换逻辑 (Token Dispatching)</h2>
                <div style="background-color: #1a1a1a; border-radius: 8px; padding: 30px; color: #00ff00; font-family: monospace; position: relative;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="border: 1px solid #00ff00; padding: 10px; text-align: center;">GPU 01<br>[T1, T2]</div>
                        <div style="flex-grow: 1; height: 2px; background: #00ff00; position: relative;">
                            <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #1a1a1a; padding: 0 10px;">Network Switch</div>
                        </div>
                        <div style="border: 1px solid #00ff00; padding: 10px; text-align: center;">GPU 02<br>[T3, T4]</div>
                    </div>
                    <div style="margin-top: 20px; text-align: center; font-size: 12px; color: #888;">
                        T1 -> Expert@GPU 02 (8KB Payload)<br>
                        T4 -> Expert@GPU 01 (8KB Payload)
                    </div>
                </div>
                <p style="font-size: 14px; color: #666; margin-top: 15px;">这是 MoE 的性能死穴。不同于传统的同步，All-to-All 要求网络在每一层计算时都进行一次<strong>“全矩阵分拣”</strong>。一旦网络带宽不足或出现拥塞，GPU 就会陷入停顿。</p>
            </div>

            <!-- Visualization 3: Vector Space -->
            <div style="margin-bottom: 50px;">
                <h2 style="font-size: 18px; border-left: 5px solid #28a745; padding-left: 15px; margin-bottom: 25px;">3. 语义向量空间 (Semantic Manifold)</h2>
                <div style="text-align: center; background: #fff; border: 1px solid #eee; border-radius: 8px; padding: 20px;">
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        <circle cx="100" cy="100" r="80" fill="none" stroke="#28a745" stroke-width="1" />
                        <line x1="20" y1="100" x2="180" y2="100" stroke="#eee" />
                        <line x1="100" y1="20" x2="100" y2="180" stroke="#eee" />
                        <!-- Clusters -->
                        <circle cx="60" cy="70" r="15" fill="rgba(40, 167, 69, 0.2)" />
                        <text x="45" y="75" font-size="10" fill="#28a745">Tech</text>
                        <circle cx="140" cy="130" r="15" fill="rgba(255, 75, 43, 0.2)" />
                        <text x="125" y="135" font-size="10" fill="#ff4b2b">Art</text>
                    </svg>
                </div>
                <p style="font-size: 14px; color: #666; margin-top: 15px;">向量在高维空间中通过<strong>聚类</strong>表征语义。MoE 路由本质上是在做“空间分割”，将落在不同区域的坐标点分配给对应的专家进行处理。</p>
            </div>

            <!-- Conclusion -->
            <div style="background: #fdfdfe; border-left: 5px solid #1a1a1a; padding: 30px; border-radius: 5px;">
                <p style="font-size: 16px; font-weight: 700; margin: 0;">星宝总结：</p>
                <p style="font-size: 15px; margin-top: 10px; color: #444;">MoE 架构将 AI 竞争从“暴力美学”推向了<strong>“调度艺术”</strong>。在物理层面，这表现为对显存带宽、卡间互联和网络协议的极致压榨。理解了这一点，就能看懂 DeepSeek 论文中为何如此强调 I/O 路径的优化。</p>
            </div>

            <!-- Footer -->
            <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; text-align: right; font-size: 12px; color: #999;">
                <p>Generated by 星宝 (Main Agent)</p>
                <p>星宝 AI</p>
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
        print("Final visual report email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    send_final_report()
