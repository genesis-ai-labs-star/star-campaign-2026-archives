# Biometric Guard - 华为手表实战方案

## 1. 核心链路：Strava 穿透
华为运动健康（加拿大/海外版）支持将数据同步至 Strava。我们将利用 Strava 开放的 API 建立自动化抓取流水线。

## 2. 自动化组件
- **数据源**：Huawei Health App -> Strava (App 内一键绑定)
- **抓取器**：`strava-harvester.py` (部署在 Mac mini，每 30 分钟运行)
- **分析引擎**：星宝 (Main) 定期读取 Strava 数据，评估 HRV、睡眠质量与心率负荷。
- **预警通道**：Telegram (@Evoway_bot) 实时推送健康熔断建议。

## 3. 司令部部署步骤
1. **用户侧**：在华为 App 绑定 Strava。
2. **星宝侧**：
   - 申请 Strava API Client ID/Secret。
   - 部署 MCP 服务器 `strava-mcp` 以实现语义化健康查询。
   - 建立 `memory/health.md` 结构化日志。

## 4. 监控指标
- **HRV (心率变异性)**：判断神经系统疲劳度。
- **睡眠得分**：决定当日进攻任务的复杂度。
- **活动消耗**：确保老段在攻坚 Genesis 时保持基础代谢。
