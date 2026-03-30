import os, re, subprocess, sys

def scan_for_secrets():
    # Basic secret scan
    for root, dirs, files in os.walk("."):
        if ".git" in dirs: dirs.remove(".git")
        if "venv" in dirs: dirs.remove("venv")
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        
        for file in files:
            file_path = os.path.join(root, file)
            if file == ".env" and os.path.exists(file_path):
                # Don't let real .env be committed natively (should be gitignored, but this is a double check)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if len(content.strip()) > 0:
                        return f"Exposed .env file detected at {file_path}"
                        
            if file.endswith(('.py', '.txt', '.md', '.json', '.yaml')):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "API_KEY" in content and "os.getenv" not in content and not file.endswith("git_sync.py") and not file.endswith("README.md"):
                            return f"Potential hardcoded API_KEY found in {file_path}"
                        if re.search(r"sk-[a-zA-Z0-9]{32,}", content):
                            return f"Potential OpenAI key (sk-...) found in {file_path}"
                        if re.search(r"[0-9]{8,10}:[a-zA-Z0-9_-]{35,}", content): # Telegram Bot Token pattern
                            return f"Potential Telegram Bot token found in {file_path}"
                except UnicodeDecodeError:
                    pass
    return None

def sync():
    secret_issue = scan_for_secrets()
    if secret_issue:
        print(f"[CRITICAL] Sync aborted due to security vulnerability: {secret_issue}")
        sys.exit(1)

    tracking_path = "docs/tracking.md"
    if not os.path.exists(tracking_path):
        print(f"[!] {tracking_path} not found. Git sync aborted.")
        return

    with open(tracking_path, "r") as f:
        lines = f.readlines()
        if not lines:
            return
            
        for line in reversed(lines):
            # Look for commit messages in the tracking table (e.g., | Date | Task | `commit message` |)
            m = re.search(r'\|\s*`([^`]+)`\s*\|', line)
            if m:
                msg = m.group(1)
                print(f"[...] Syncing changes with commit: {msg}")
                subprocess.run("git add .", shell=True)
                subprocess.run(f'git commit -m "{msg}"', shell=True)
                subprocess.run("git push origin main", shell=True)
                return

if __name__ == "__main__":
    sync()
