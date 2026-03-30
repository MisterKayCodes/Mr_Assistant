import os
import subprocess
import shutil

# --- TEST SETUP ---
TEST_DIR = "constitution_fire_drill"

TEST_CASES = {
    "bad_rule12_silent.py": """
try:
    x = 1/0
except:
    pass # Rule 12 Violation
""",
    "bad_rule12_exception.py": """
try:
    x = 1/0
except Exception:
    pass # Rule 12 Violation
""",
    "bad_rule14_openai.py": """
# Security leak!
api_key = "sk-T0ken12345678901234567890" # Rule 14 Violation
""",
    "bad_rule14_telegram.py": """
BOT_TOKEN = "123456789:ABCDefghIJKLmnopQRSTuvwxyz123456789" # Rule 14 Violation
""",
    "bad_rule8_spaghetti.py": """
# Rule 8 Violation (Nesting depth 5)
if True:
    if True:
        if True:
            if True:
                if True:
                    print("Spaghetti!")
""",
    "bad_rule3_mix.py": """
import aiogram
import sqlalchemy # Rule 3 Violation: Mixing layers

async def main():
    pass
""",
    "bad_rule3_mega.py": "\n".join([f"# Line {i}" for i in range(305)]), # Rule 3 Violation (> 300 lines)

    "good_code.py": """
import aiogram
import logging

# Senior-level code
async def main():
    try:
        print("Hello Law!")
    except Exception as e:
        logging.error(f"Handled error: {e}")
""",
    "requirements.txt": """
aiogram>=3.0
sqlalchemy # Rule 13 Violation: Unpinned
aiosqlite==0.19.0
"""
}

def setup_tests():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    
    for filename, content in TEST_CASES.items():
        with open(os.path.join(TEST_DIR, filename), "w") as f:
            f.write(content)

import sys

def run_constitution():
    print(f"--- Starting Fire Drill: Running Constitution against {len(TEST_CASES)} tests ---\n")
    # Use sys.executable for cross-platform reliability
    cmd = [sys.executable, "scripts/dev_constitution.py", "--dir", TEST_DIR]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return result.stdout, result.returncode

def main():
    setup_tests()
    output, exit_code = run_constitution()
    
    # Verify violations
    print(output)
    violations_found = output.count("[X]")
    
    print("-" * 30)
    print(f"Summary: Found {violations_found} violations.")
    
    # Check if specific violations were caught
    expected_violations = 8 # (7 bad py files + 1 unpinned requirement)
    if violations_found >= expected_violations:
        print("SUCCESS: The Constitution caught the expected crimes!")
    else:
        print(f"FAILURE: Expected {expected_violations} violations, found {violations_found}.")

    # Cleanup
    # shutil.rmtree(TEST_DIR) # Comment out if you want to inspect bad files

if __name__ == "__main__":
    main()
