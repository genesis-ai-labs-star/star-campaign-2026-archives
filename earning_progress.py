import os

def check_progress():
    workspace = "/Users/genesis/.openclaw/workspace"
    # Look for files related to earning or bounties
    potential_files = ["BOUNTY.md", "EARNINGS.md", "MONEY.md", "GOALS.md"]
    found = False
    for f in potential_files:
        path = os.path.join(workspace, f)
        if os.path.exists(path):
            print(f"--- {f} ---")
            with open(path, 'r') as file:
                print(file.read())
            found = True
    
    if not found:
        print("No specific earnings tracking file found in workspace root.")
        # Check memory directory for mentions
        memory_dir = os.path.join(workspace, "memory")
        if os.path.exists(memory_dir):
            print("\nScanning memory for '$1000'...")
            os.system(f"grep -r '\$1000' {memory_dir}")

check_progress()
