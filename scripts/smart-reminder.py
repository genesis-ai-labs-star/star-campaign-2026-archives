import json
import os
from datetime import datetime
import pytz

def smart_remind():
    state_path = "/Users/genesis/.openclaw/workspace/state/reminder-state.json"
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    
    itinerary = [
        ("2026-02-01", "Ottawa", "America/Toronto"),
        ("2026-02-28", "Shenzhen", "Asia/Shanghai")
    ]
    
    now_utc = datetime.now(pytz.utc)
    current_tz_str = "America/Toronto"
    current_loc = "Ottawa"
    
    for start_date_str, loc, tz in sorted(itinerary, key=lambda x: x[0], reverse=True):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        if now_utc >= start_date:
            current_tz_str = tz
            current_loc = loc
            break
            
    local_tz = pytz.timezone(current_tz_str)
    now_local = datetime.now(local_tz)
    
    print(f"Current Location: {current_loc} | Local Time: {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    if now_local.hour == 9:
        today_str = now_local.strftime("%Y-%m-%d")
        state = {}
        if os.path.exists(state_path):
            with open(state_path, "r") as f:
                state = json.load(f)
        
        if state.get("last_reminded_date") != today_str:
            # V1.4.5 Upgrade: Use direct message send to avoid Session overflow issues
            message = f"🔔 老段，现在是 {current_loc} 时间上午 9 点。该打卡上班了！"
            # Target is your Telegram ID
            cmd = f'openclaw message send --channel telegram --target "8534135698" --message "{message}"'
            os.system(cmd)
            
            state["last_reminded_date"] = today_str
            state["location"] = current_loc
            with open(state_path, "w") as f:
                json.dump(state, f)
            print("Direct reminder sent.")
    else:
        print("Not 9:00 AM window.")

if __name__ == "__main__":
    smart_remind()
