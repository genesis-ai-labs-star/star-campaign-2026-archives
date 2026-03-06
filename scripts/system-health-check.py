import subprocess
import re
import os

def get_memory_stats():
    try:
        # Get vm_stat output
        vm = subprocess.check_output(['vm_stat']).decode('utf-8')
        # Extract page size - handling the parenthesis format
        page_size_match = re.search(r'page size of (\d+) bytes', vm)
        if not page_size_match:
            return "Error: Could not find page size"
        page_size = int(page_size_match.group(1))
        
        # Extract free pages
        free_pages_match = re.search(r'Pages free:\s+(\d+)', vm)
        if not free_pages_match:
            return "Error: Could not find free pages"
        free_pages = int(free_pages_match.group(1))
        
        free_gb = (free_pages * page_size) / (1024**3)
        return f"Memory Free: {free_gb:.2f} GB"
    except Exception as e:
        return f"Memory Check Error: {e}"

if __name__ == "__main__":
    print(get_memory_stats())
