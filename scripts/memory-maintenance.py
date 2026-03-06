import json
import os
from datetime import datetime, timedelta

WORKSPACE_DIR = "/Users/genesis/.openclaw/workspace"
MEMORY_DIR = os.path.join(WORKSPACE_DIR, "memory")
STATE_FILE = os.path.join(MEMORY_DIR, "heartbeat-state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"lastChecks": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def run_maintenance():
    state = load_state()
    last_run_str = state.get("lastMemoryMaintenance")
    
    if last_run_str:
        last_run = datetime.strptime(last_run_str, "%Y-%m-%d")
        if datetime.now() - last_run < timedelta(days=7):
            print(f"Maintenance already run on {last_run_str}. Skipping.")
            return

    print("🕒 Starting Weekly Memory Maintenance...")
    
    # 1. Read last 7 days of logs
    # 2. Extract long-term value to projects.md, infra.md, lessons.md
    # 3. Compress old logs (This would usually be an LLM task, so we emit a prompt)
    
    print("MISSION: [Weekly Memory Maintenance]")
    print("- Reading recent logs...")
    print("- Distilling projects.md, infra.md, lessons.md...")
    print("- Archiving temporary notes...")
    
    # Update state
    state["lastMemoryMaintenance"] = datetime.now().strftime("%Y-%m-%d")
    save_state(state)
    print("✅ Maintenance task logged.")

if __name__ == "__main__":
    run_maintenance()
