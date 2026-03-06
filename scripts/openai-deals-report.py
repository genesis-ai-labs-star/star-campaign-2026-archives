#!/usr/bin/env python3
"""
OpenAI New Deals Analysis Report
Target: hello.duan@foxmail.com
"""

import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.openclaw/.env'))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 465
SMTP_USER = os.environ['FOXMAIL_USER']
SMTP_PASS = os.environ['FOXMAIL_PASSWORD']

html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenAI 新协议战略分析报告</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif; background: #0f0f13; color: #e0e0e0; }
  .wrapper { max-width: 680px; margin: 0 auto; padding: 24px 16px; }
  
  .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border-radius: 16px; padding: 32px 28px; margin-bottom: 24px; border: 1px solid #1e3a5f; }
  .header-badge { display: inline-block; background: rgba(99,179,237,0.15); border: 1px solid #63b3ed; color: #63b3ed; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; padding: 4px 12px; border-radius: 20px; margin-bottom: 16px; text-transform: uppercase; }
  .header-title { font-size: 22px; font-weight: 800; color: #ffffff; line-height: 1.3; margin-bottom: 10px; }
  .header-subtitle { font-size: 13px; color: #8899aa; line-height: 1.6; }
  .header-meta { margin-top: 16px; display: flex; gap: 16px; flex-wrap: wrap; }
  .meta-tag { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #aabbcc; }

  .tldr { background: linear-gradient(135deg, rgba(99,179,237,0.1), rgba(139,92,246,0.1)); border: 1px solid rgba(99,179,237,0.3); border-radius: 12px; padding: 20px 22px; margin-bottom: 20px; }
  .tldr-label { font-size: 10px; letter-spacing: 2px; color: #63b3ed; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; }
  .tldr-text { font-size: 15px; color: #e8f4f8; line-height: 1.7; font-weight: 500; }

  .section { background: #16161d; border: 1px solid #2a2a3a; border-radius: 12px; padding: 22px; margin-bottom: 16px; }
  .section-title { font-size: 13px; font-weight: 700; color: #63b3ed; letter-spacing: 0.5px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; text-transform: uppercase; }
  
  .company-card { background: #1a1a25; border-radius: 10px; padding: 16px 18px; margin-bottom: 12px; border-left: 3px solid; }
  .company-card.nvda { border-left-color: #76b900; }
  .company-card.msft { border-left-color: #0078d4; }
  .company-card.amzn { border-left-color: #ff9900; }
  .company-card.openai { border-left-color: #10a37f; }
  .company-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .company-name { font-size: 14px; font-weight: 700; color: #ffffff; }
  .company-ticker { font-size: 11px; color: #888; background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 4px; }
  .impact-badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
  .impact-positive { background: rgba(118,185,0,0.15); color: #76b900; border: 1px solid rgba(118,185,0,0.3); }
  .impact-neutral { background: rgba(255,165,0,0.15); color: #ffa500; border: 1px solid rgba(255,165,0,0.3); }
  .impact-negative { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
  .company-points { list-style: none; }
  .company-points li { font-size: 13px; color: #c0c0d0; line-height: 1.7; padding: 3px 0; padding-left: 14px; position: relative; }
  .company-points li::before { content: "›"; position: absolute; left: 0; color: #63b3ed; font-weight: 700; }

  .deal-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .deal-item { background: #1a1a25; border-radius: 10px; padding: 14px 16px; border: 1px solid #2a2a3a; }
  .deal-amount { font-size: 20px; font-weight: 800; color: #63b3ed; }
  .deal-label { font-size: 11px; color: #7788aa; margin-top: 4px; }
  .deal-detail { font-size: 12px; color: #aabbcc; margin-top: 8px; line-height: 1.5; }

  .signal-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #2a2a3a; }
  .signal-row:last-child { border-bottom: none; }
  .signal-label { font-size: 13px; color: #c0c0d0; }
  .signal-value { font-size: 13px; font-weight: 600; }
  .signal-bull { color: #76b900; }
  .signal-bear { color: #ef4444; }
  .signal-neutral { color: #ffa500; }

  .action-card { background: linear-gradient(135deg, rgba(118,185,0,0.08), rgba(99,179,237,0.08)); border: 1px solid rgba(118,185,0,0.25); border-radius: 12px; padding: 20px 22px; margin-bottom: 16px; }
  .action-item { display: flex; gap: 12px; margin-bottom: 14px; align-items: flex-start; }
  .action-item:last-child { margin-bottom: 0; }
  .action-num { background: #63b3ed; color: #0f0f13; font-size: 11px; font-weight: 800; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
  .action-text { font-size: 13px; color: #c8d8e8; line-height: 1.6; }
  .action-text strong { color: #ffffff; }

  .risk-item { background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; font-size: 13px; color: #ffaaaa; line-height: 1.6; }

  .footer { text-align: center; padding: 20px; }
  .footer-text { font-size: 11px; color: #445566; line-height: 1.8; }
  .footer-sig { font-size: 12px; color: #556677; margin-top: 8px; }

  @media (max-width: 480px) {
    .deal-grid { grid-template-columns: 1fr; }
    .company-header { flex-direction: column; align-items: flex-start; gap: 6px; }
    .header-title { font-size: 18px; }
  }
</style>
</head>
<body>
<div class="wrapper">

  <!-- Header -->
  <div class="header">
    <div class="header-badge">⚡ 战略情报 · 即时分析</div>
    <div class="header-title">OpenAI 新融资协议：对 Amazon、Microsoft、NVIDIA 的战略冲击</div>
    <div class="header-subtitle">基于 The Information 独家报道 + 公开市场数据的综合研判<br>情报来源：The Information (2026-02-27) | 分析师：星宝</div>
    <div class="header-meta">
      <span class="meta-tag">📅 2026-02-27</span>
      <span class="meta-tag">🏷️ NVDA · MSFT · AMZN · OPENAI</span>
      <span class="meta-tag">🎯 AI 算力基础设施赛道</span>
    </div>
  </div>

  <!-- TL;DR -->
  <div class="tldr">
    <div class="tldr-label">📌 核心结论 (TL;DR)</div>
    <div class="tldr-text">
      OpenAI 完成约 $1,100 亿融资，引入 Amazon 作为重要云算力合作方。
      这一格局重组的本质是：<strong>微软的独家地位被打破，Amazon 云业务意外受益，NVIDIA 算力需求不减反增</strong>。
      对投资者而言，这是 AI 军备竞赛加速的信号，而非市场见顶。
    </div>
  </div>

  <!-- Deal Numbers -->
  <div class="section">
    <div class="section-title">💰 协议关键数字</div>
    <div class="deal-grid">
      <div class="deal-item">
        <div class="deal-amount">$1,100亿</div>
        <div class="deal-label">OpenAI 融资总规模</div>
        <div class="deal-detail">全球历史上最大规模的科技公司单轮融资之一</div>
      </div>
      <div class="deal-item">
        <div class="deal-amount">$500亿</div>
        <div class="deal-label">Amazon 承诺投入</div>
        <div class="deal-detail">以 AWS 算力采购 + 战略股权形式注入，含 IPO/AGI 触发条款</div>
      </div>
      <div class="deal-item">
        <div class="deal-amount">$111亿</div>
        <div class="deal-label">OpenAI 预测 2030 前现金消耗</div>
        <div class="deal-detail">算力军备竞赛的实质成本，对 GPU 供应商是持续利好</div>
      </div>
      <div class="deal-item">
        <div class="deal-amount">多方</div>
        <div class="deal-label">云平台布局</div>
        <div class="deal-detail">Azure (微软) + AWS (亚马逊) + Stargate (SoftBank/甲骨文) 三足鼎立</div>
      </div>
    </div>
  </div>

  <!-- Company Impact Analysis -->
  <div class="section">
    <div class="section-title">🏢 各公司战略影响拆解</div>

    <div class="company-card nvda">
      <div class="company-header">
        <span class="company-name">NVIDIA</span>
        <span class="company-ticker">NVDA</span>
        <span class="impact-badge impact-positive">📈 强烈利好</span>
      </div>
      <ul class="company-points">
        <li>OpenAI 耗资 $1,100 亿的背后，是对 H100/H200/B200 GPU 集群的持续海量采购。</li>
        <li>Amazon AWS 加入意味着多一条"算力买单"路径，NVDA 的需求不会因云平台竞争而受损——反而会因多个平台争夺 OpenAI 份额而激增。</li>
        <li>Stargate 项目（SoftBank + OpenAI）单独的算力基础设施需求也在持续扩张。</li>
        <li><strong>结论</strong>：OpenAI 多云策略 = 多个金主同时买 NVDA 的卡。</li>
      </ul>
    </div>

    <div class="company-card msft">
      <div class="company-header">
        <span class="company-name">Microsoft</span>
        <span class="company-ticker">MSFT</span>
        <span class="impact-badge impact-neutral">⚠️ 中性偏负</span>
      </div>
      <ul class="company-points">
        <li>微软失去"OpenAI 独家云合作伙伴"光环，这是过去两年估值溢价的重要来源。</li>
        <li>Azure 仍是 OpenAI 的首要云平台，但护城河变窄，多云布局分散了 Azure 的独占优势。</li>
        <li>微软仍持有 OpenAI 约 49% 的股权结构利润分配权，上行依然存在，但需要重新定价。</li>
        <li><strong>结论</strong>：短期承压，但不构成基本面崩塌。股价若继续回调可视为吸筹机会。</li>
      </ul>
    </div>

    <div class="company-card amzn">
      <div class="company-header">
        <span class="company-name">Amazon</span>
        <span class="company-ticker">AMZN</span>
        <span class="impact-badge impact-positive">📈 战略受益</span>
      </div>
      <ul class="company-points">
        <li>$500 亿 AWS 算力采购协议，为 AWS AI 业务提供了一个"镇店之宝"级战略锚点。</li>
        <li>此前 AWS 在 AI 基础模型赛道落后于 Azure，此次与 OpenAI 深度绑定，直接补齐了最大短板。</li>
        <li>含 IPO/AGI 里程碑触发条款，意味着协议深度绑定，不是简单的"买云服务"。</li>
        <li><strong>结论</strong>：AWS AI 战略转折点。看好中长期估值重估，是本次协议最大的"意外赢家"。</li>
      </ul>
    </div>

    <div class="company-card openai">
      <div class="company-header">
        <span class="company-name">OpenAI (未上市)</span>
        <span class="company-ticker">私有</span>
        <span class="impact-badge impact-positive">🚀 战略扩张</span>
      </div>
      <ul class="company-points">
        <li>通过多云布局（Azure + AWS + Stargate）掌握了对各大云平台的议价权。</li>
        <li>$111 亿的预期现金消耗是清醒的战略投入，而非亏损危机信号。</li>
        <li>当前估值可能已达 $2,000 亿+，IPO 前景受到高度关注。</li>
      </ul>
    </div>
  </div>

  <!-- Market Signals -->
  <div class="section">
    <div class="section-title">📊 市场信号速查</div>
    <div class="signal-row">
      <span class="signal-label">AI 算力需求趋势</span>
      <span class="signal-value signal-bull">↑ 持续加速</span>
    </div>
    <div class="signal-row">
      <span class="signal-label">NVDA GPU 需求展望</span>
      <span class="signal-value signal-bull">↑ 多方买单，需求无忧</span>
    </div>
    <div class="signal-row">
      <span class="signal-label">Azure 独占溢价</span>
      <span class="signal-value signal-bear">↓ 收窄，需重新定价</span>
    </div>
    <div class="signal-row">
      <span class="signal-label">AWS AI 战略地位</span>
      <span class="signal-value signal-bull">↑ 显著提升</span>
    </div>
    <div class="signal-row">
      <span class="signal-label">AI 军备竞赛阶段</span>
      <span class="signal-value signal-neutral">加速期（非泡沫顶部）</span>
    </div>
    <div class="signal-row">
      <span class="signal-label">互联网络/交换机需求 (AVGO/MRVL)</span>
      <span class="signal-value signal-bull">↑ 随算力需求同步扩张</span>
    </div>
  </div>

  <!-- Action Playbook -->
  <div class="action-card">
    <div class="section-title" style="margin-bottom:14px;">🎯 投资行动手册 (Questrade 适配)</div>
    <div class="action-item">
      <div class="action-num">1</div>
      <div class="action-text"><strong>持有/加仓 NVDA</strong>：多云格局意味着多金主争抢算力，$178 附近的回调是绝佳机会。OpenAI 的 $111B 现金消耗路径，就是 NVDA 的未来订单簿。</div>
    </div>
    <div class="action-item">
      <div class="action-num">2</div>
      <div class="action-text"><strong>关注 AMZN 逢低机会</strong>：AWS 绑定 OpenAI 是季度级别的催化剂，但需等待市场消化后的回调入场点，建议观察 Q1 财报电话会对 AWS AI 收入指引。</div>
    </div>
    <div class="action-item">
      <div class="action-num">3</div>
      <div class="action-text"><strong>MSFT 降低权重</strong>：独家光环消失后需重新评估 AI 溢价部分。基本面仍稳，但短期催化剂减弱，可将仓位向 NVDA/AMZN 倾斜。</div>
    </div>
    <div class="action-item">
      <div class="action-num">4</div>
      <div class="action-text"><strong>配置 SMH/SOXX ETF 作为底仓</strong>：无论哪个云平台赢，算力芯片（NVDA + AVGO + MRVL）是确定性受益方。ETF 可降低单股风险。</div>
    </div>
  </div>

  <!-- Risk Factors -->
  <div class="section">
    <div class="section-title">⚠️ 关键风险因子</div>
    <div class="risk-item">🔴 <strong>AGI 触发条款</strong>：Amazon 的 $500B 协议含 AGI/IPO 里程碑条件，若 OpenAI 进展不及预期，协议规模可能缩水。</div>
    <div class="risk-item">🟡 <strong>Stargate 资金压力</strong>：SoftBank 主导的 Stargate 项目融资进展缓慢，若出现延期，算力投入节奏可能放缓。</div>
    <div class="risk-item">🟡 <strong>监管与反垄断</strong>：多家巨头同时深度绑定 OpenAI，可能引发欧盟/FTC 监管审查，增加不确定性。</div>
    <div class="risk-item">🔴 <strong>DeepSeek 效应</strong>：若 MoE 等高效架构大规模普及，算力需求增速可能被"效率提升"部分抵消，但短期内影响有限。</div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <div class="footer-text">
      本报告基于公开信息综合分析，不构成具体投资建议<br>
      情报来源：The Information | 分析时间：2026-02-27 16:15 EST
    </div>
    <div class="footer-sig">— 星宝 AI | 为老段定制</div>
  </div>

</div>
</body>
</html>"""

msg = MIMEMultipart('alternative')
msg['Subject'] = f"⚡ 战略情报 | OpenAI 新协议：Amazon 赢家、微软失色、NVDA 不变 [{datetime.now().strftime('%Y-%m-%d')}]"
msg['From'] = f"星宝 <{SMTP_USER}>"
msg['To'] = "hello.duan@foxmail.com"
msg.attach(MIMEText(html, 'html', 'utf-8'))

with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as s:
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, ["hello.duan@foxmail.com"], msg.as_string())

print("✅ 报告已发送至 hello.duan@foxmail.com")
