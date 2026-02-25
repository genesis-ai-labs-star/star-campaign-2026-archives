import sys
import subprocess

def think(prompt):
    try:
        result = subprocess.run(['ollama', 'run', 'deepseek-r1:14b', prompt], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"DeepSeek Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(think(sys.argv[1]))
