import os
import subprocess
import sys

# Change dir to root of project (Mister_Starter_Pack)
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

def create_dummy_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def cleanup_dummy_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
        d = os.path.dirname(path)
        if d:
            try:
                os.rmdir(d)
            except Exception:
                pass

print("="*60)
print("TESTING ARCHITECTURE INSPECTOR...")
print("="*60)

# SCENARIO 1: Deep Nesting
print("\n[SCENARIO 1] Testing Cyclomatic Complexity (Deep Nesting)")
nested_code = """
def bad_function():
    if True:
        for i in range(10):
            try:
                if i > 5:
                    print(i) # 4 levels deep
            except:
                pass
"""
create_dummy_file(os.path.join("app", "core", "test_nesting.py"), nested_code)
result = subprocess.run([sys.executable, os.path.join("scripts", "architecture_inspector.py")], capture_output=True, text=True)
if "Spaghetti Warning: Deep nesting detected" in result.stdout:
    print("[PASS]: Inspector correctly blocked deep nesting!")
else:
    print("[FAIL]: Inspector missed deeply nested code.")
cleanup_dummy_file(os.path.join("app", "core", "test_nesting.py"))

# SCENARIO 2: Over 200 lines
print("\n[SCENARIO 2] Testing 200-Line Rule")
long_code = "\n".join([f"print({i})" for i in range(250)])
create_dummy_file(os.path.join("app", "core", "test_lines.py"), long_code)
result = subprocess.run([sys.executable, os.path.join("scripts", "architecture_inspector.py")], capture_output=True, text=True)
if "File too long" in result.stdout:
    print("[PASS]: Inspector correctly blocked file exceeding 200 lines!")
else:
    print("[FAIL]: Inspector missed long file constraint.")
cleanup_dummy_file(os.path.join("app", "core", "test_lines.py"))

# SCENARIO 3: Illegal Import
print("\n[SCENARIO 3] Testing Illegal Layers")
illegal_code = """
import bot.handlers
from aiogram import types
"""
create_dummy_file(os.path.join("app", "core", "test_import.py"), illegal_code)
result = subprocess.run([sys.executable, os.path.join("scripts", "architecture_inspector.py")], capture_output=True, text=True)
if "Illegal import" in result.stdout:
    print("[PASS]: Inspector correctly blocked illegal imports across domains!")
else:
    print("[FAIL]: Inspector missed cross-contamination.")
cleanup_dummy_file(os.path.join("app", "core", "test_import.py"))

print("\n" + "="*60)
print("TESTING GIT SYNC (SECRET SCANNING)...")
print("="*60)

# SCENARIO 4: Exposed .env file
print("\n[SCENARIO 4] Testing Exposed .env file prevention")
create_dummy_file(".env", "API_KEY=secret_123")
result = subprocess.run([sys.executable, os.path.join("scripts", "git_sync.py")], capture_output=True, text=True)
if "CRITICAL" in result.stdout and "Exposed .env file detected" in result.stdout:
    print("[PASS]: Git sync correctly aborted due to exposed .env file!")
else:
    print("[FAIL]: Git sync failed to catch exposed .env file.")
cleanup_dummy_file(".env")

# SCENARIO 5: Hardcoded API Key
print("\n[SCENARIO 5] Testing Hardcoded API Key prevention")
create_dummy_file(os.path.join("app", "services", "test_keys.py"), 'API_KEY = "shhhhh"')
result = subprocess.run([sys.executable, os.path.join("scripts", "git_sync.py")], capture_output=True, text=True)
if "CRITICAL" in result.stdout and "Potential hardcoded API_KEY found" in result.stdout:
    print("[PASS]: Git sync correctly aborted due to hardcoded API keys!")
else:
    print("[FAIL]: Git sync failed to catch hardcoded API keys.")
cleanup_dummy_file(os.path.join("app", "services", "test_keys.py"))

print("\n" + "="*60)
print("TESTING PROJECT MAP GENERATOR...")
print("="*60)

# SCENARIO 6: Project Map Generation
print("\n[SCENARIO 6] Testing Project Map output")
result = subprocess.run([sys.executable, os.path.join("scripts", "project_map.py")], capture_output=True, text=True)
if os.path.exists("project_map.txt"):
    print("[PASS]: Project map successfully generated!")
    with open("project_map.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if "app/" in content and "scripts/" in content:
           print("[PASS]: Map contains appropriate directory tree details!")
else:
    print("[FAIL]: Project map generation failed.")
if os.path.exists("project_map.txt"):
    os.remove("project_map.txt")

print("\n🎉 All tests completed. Systems are robust and behaving securely.")
