# SYSTEM_STANDARDS.md - 星宝系统指标统计规范

## 1. 内存统计规范 (Memory Reporting)
- **核心逻辑**：严禁硬编码 `4096`。必须通过 `pagesize` 命令获取实时页大小。
- **计算公式**：`可用内存 (Available) = (Pages free + Pages speculative) * pagesize / 1024 / 1024` (单位: MB)。
- **口径定义**：
  - **物理空闲 (Strictly Free)**：仅包含 `Pages free` + `Pages speculative`。
  - **压缩水位 (Compressed)**：显示 `Pages stored in compressor` 的大小，作为“潜在可用”参考。
- **预警阈值**：
  - **软预警 (Soft)**：可用内存 < 500MB，执行静默 `purge`。
  - **硬预警 (Hard)**：可用内存 < 200MB，Telegram 告警并准备重启。

## 2. CPU 与负载统计 (CPU & Load)
- **Load Avg**：直接引用 `uptime` 或 `top` 的 1/5/15 分钟均值。
- **使用率**：区分 `User` 与 `System` 占比，突出“算力余量”。

## 3. 磁盘与 IO (Storage)
- **可用空间**：统一使用 `Gi` 为单位，保留整数。
- **路径监控**：核心监控 `/Users/genesis` 所在分区的健康度。

## 4. 执行约束
- 所有自动化脚本 (`watchdog.sh`, `purger.sh`, `generate-report.py`) 必须对齐上述逻辑。
- 每次 Session 启动，Agent 必须读取此文件以校准汇报口径。
