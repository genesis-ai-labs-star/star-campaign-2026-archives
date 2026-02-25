import os
import json
import glob

def map_context():
    workspaces = [
        "/Users/genesis/.openclaw/workspace",
        "/Users/genesis/.openclaw/workspace-investor",
        "/Users/genesis/.openclaw/workspace-life"
    ]
    
    context_map = {
        "last_updated": os.popen("date").read().strip(),
        "workspaces": {},
        "active_goals": [],
        "critical_issues": []
    }

    for ws in workspaces:
        ws_name = os.path.basename(ws)
        if os.path.exists(ws):
            # Get last modified memory file
            memory_files = glob.glob(f"{ws}/memory/*.md")
            latest_memory = max(memory_files, key=os.path.getmtime) if memory_files else None
            
            # Check for specific tracking files
            has_bounties = os.path.exists(f"{ws}/bounties.md")
            has_progress = os.path.exists(f"{ws}/earning_progress.py")
            
            context_map["workspaces"][ws_name] = {
                "path": ws,
                "latest_memory": os.path.basename(latest_memory) if latest_memory else None,
                "has_bounties": has_bounties,
                "has_progress": has_progress
            }

    # Store the map
    map_path = "/Users/genesis/.openclaw/workspace/config/context-map.json"
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w") as f:
        json.dump(context_map, f, indent=2)
    
    print(f"Context map updated at {map_path}")

if __name__ == "__main__":
    map_context()
