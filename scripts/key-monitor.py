import os
import json

def check_investor_errors():
    ws_investor = "/Users/genesis/.openclaw/workspace-investor"
    log_path = f"{ws_investor}/cron.log"
    
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            lines = f.readlines()
            # Look for common error patterns
            errors = [line for line in lines[-50:] if "error" in line.lower() or "failed" in line.lower()]
            if errors:
                print(f"Found {len(errors)} potential issues in investor logs.")
                # Logic to rotate keys or alert would go here
                return errors
    return []

if __name__ == "__main__":
    issues = check_investor_errors()
    if issues:
        # Update context map with critical issues
        map_path = "/Users/genesis/.openclaw/workspace/config/context-map.json"
        with open(map_path, "r") as f:
            data = json.load(f)
        data["critical_issues"] = issues
        with open(map_path, "w") as f:
            json.dump(data, f, indent=2)
        print("Critical issues synced to S.M. brain.")
