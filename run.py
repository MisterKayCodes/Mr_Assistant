import subprocess, sys, os, time

def run_inspector():
    print("[...] Running Architecture Inspector...")
    try:
        # We run the inspector as a separate process to keep everything clean.
        result = subprocess.run([sys.executable, "scripts/core/architecture_inspector.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Architecture inspection passed.")
            return True
        else:
            print("[!] Architecture inspection failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[!] Error running inspector: {e}")
        return False

def kill_ghosts():
    print("[...] Searching for and terminating ghost processes...")
    try:
        if os.name == 'nt':
            # SURGICAL SEARCH: Find and kill only Python processes belonging to THIS bot.
            cmd = "powershell -Command \"Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*Mr_Assistant*main.py*' -or $_.CommandLine -like '*Mr_Assistant*run.py*' } | Stop-Process -Force -ErrorAction SilentlyContinue\""
            subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        else:
            cmd = 'pkill -f "Mr_Assistant.*(main|run).py"' 
            subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("[OK] Ghost processes cleared.")
    except Exception as e:
        pass

def start_bot():
    """
    Spawns the bot process with unbuffered output to ensure we see every log line.
    """
    # -u ensures Python doesn't buffer the output.
    return subprocess.Popen([sys.executable, "-u", "main.py"])

if __name__ == "__main__":
    if run_inspector():
        kill_ghosts()
        
        print("\n" + "="*50)
        print("[LIBRARIAN REMINDER] Did you update docs/tracking.md?")
        print("[LIBRARIAN REMINDER] Did you record 'why' in personal/learning.md?")
        print("="*50 + "\n")
        
        try:
            from watchfiles import watch
            
            # THE AXE FILTER: Built for Senior Hot-Swapping.
            def senior_filter(change, path):
                # Normalize slashes for Windows consistency.
                p = path.replace("\\", "/").lower()
                
                # NOISE PROTECTION: These folders never trigger a restart.
                ignore_dirs = ["/logs/", "/storage/", "/venv/", "/.git/", "/__pycache__/", "/scripts/core/"]
                
                # NOTE PROTECTION: Writing logs/notes shouldn't reboot the organism.
                ignore_paths = ["personal/learning.md", "docs/task.md", "docs/tracking.md"]
                
                # ALLOWANCE: .env must ALWAYS trigger a restart.
                if ".env" in p:
                    return True
                    
                # Check for ignored directories or specific files.
                return not (
                    any(ign in p for ign in ignore_dirs) or 
                    any(ign in p for ign in ignore_paths)
                )
            
            print("[...] Starting bot with manual Hot-Reload loop (Loud & Proud Mode)...")
            bot_process = start_bot()
            
            # Initial Liveliness Check
            time.sleep(2)
            if bot_process.poll() is not None:
                print("[!] Bot process died instantly on startup. Exit code:", bot_process.returncode)
            
            # The Hot-Reload Watch Loop
            for changes in watch("./", watch_filter=senior_filter):
                print(f"[!] Change detected: {changes}. Restarting bot...")
                
                # Cleanup the old process
                bot_process.terminate()
                try:
                    bot_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    bot_process.kill()
                
                # Start fresh
                bot_process = start_bot()
                time.sleep(2)
                if bot_process.poll() is not None:
                    print("[!] Bot process died on restart. Exit code:", bot_process.returncode)
                
        except ImportError:
            print("[...] Installing 'watchfiles' dependency...")
            subprocess.run([sys.executable, "-m", "pip", "install", "watchfiles"])
            print("[!] Please run run.bat again to start the hardened loop.")
            sys.exit(0)
    else:
        print("[!] Fix architectural issues before running.")
        sys.exit(1)
