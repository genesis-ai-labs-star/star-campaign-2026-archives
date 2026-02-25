import json
import os

def generate_report():
    map_path = "/Users/genesis/.openclaw/workspace/config/context-map.json"
    evolution_path = "/Users/genesis/.openclaw/workspace/EVOLUTION.md"
    
    # Extract version
    version = "v1.3.0"
    if os.path.exists(evolution_path):
        with open(evolution_path, "r") as f:
            for line in f:
                if "### [" in line and "v" in line:
                    version = line.split("]")[1].strip()
                    break

    report = f"### 📊 星宝进化看板 ({version})\n"
    report += f"**汇报时间**: {os.popen('date').read().strip()}\n\n"
    
    report += "#### 1. 核心能力\n"
    report += "- 全域感知 (Neural Link)\n- 自愈哨兵 (Sentinel)\n- 系统驻留 (Ghost Protocol)\n\n"
    
    report += "#### 2. 赚钱目标进度\n"
    report += "- 目标: $1000\n- 当前: $0\n- 状态: Expensify Proposal 提交中\n\n"
    
    report += "--- \n*本报告由 S.M. 核心自动生成*"
    
    # Use sessions_send to send to main session (Telegram)
    # We need to find the session key for 'main'
    os.system(f'openclaw sessions send --label main "{report}"')

if __name__ == "__main__":
    generate_report()
