import sqlite3
import os
from datetime import datetime

# THE IDEA AUDITOR: The "X-Ray" vision for the Brain.
# Rules strictly followed: Standalone, Read-only, Observability.

DB_PATH = "storage/app.sqlite"

def view_ideas():
    if not os.path.exists(DB_PATH):
        print(f"[!] Error: Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query only the bits we care about: The inspirations.
        query = "SELECT id, timestamp, user_id, raw_text FROM messages WHERE type = 'idea' ORDER BY timestamp DESC"
        cursor.execute(query)
        ideas = cursor.fetchall()

        if not ideas:
            print("\n[?] The Vault is empty. Send some #idea messages to the bot first!")
            return

        print("\n" + "="*80)
        print(f"{'ID':<4} | {'TIMESTAMP (UTC)':<20} | {'USER':<12} | {'IDEA'}")
        print("-" * 80)

        for idea in ideas:
            idx, ts, user, text = idea
            # Truncate text for the table view
            display_text = (text[:100] + '...') if len(text) > 100 else text
            print(f"{idx:<4} | {ts[:19]:<20} | {user:<12} | {display_text}")

        print("="*80)
        print(f"Total Inspirations Captured: {len(ideas)}\n")

    except Exception as e:
        print(f"[!] Warning: Failed to access the vault: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    view_ideas()
