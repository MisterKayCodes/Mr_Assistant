import asyncio
import sys
import os

# Add project root to path so we can import our config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.gpt import gpt_service
from config import config

async def diagnostic():
    print("\n" + "="*50)
    print("🚀 MR. ASSISTANT: GPT DIAGNOSTIC")
    print("="*50 + "\n")

    # 1. Check Config
    if not config.openai_api_key or config.openai_api_key == "your_key_here":
        print("[!] Error: No OpenAI API Key found in .env!")
        print("Please paste your key into .env and try again.")
        return

    print(f"[*] API Key detected: {config.openai_api_key[:8]}... (Masked for safety)")
    
    # 2. Test Connection
    print("[...] Contacting OpenAI (gpt-4o-mini)...")
    try:
        result = await gpt_service.summarize_idea("Build a solar powered coffee machine.")
        print("\n[OK] Connection Successful!")
        print("-" * 30)
        print("SAMPLE SUMMARY DATA:")
        print(f"Summary: {result.get('summary')}")
        print(f"Category: {result.get('category')}")
        print(f"Action Points: {', '.join(result.get('action_points', []))}")
        print("-" * 30)
        print("\n[RESULT] Your brain is now officially augmented! 🧠🦾")
        
    except Exception as e:
        print(f"\n[!] Connection Failed: {e}")
        print("Check your internet connection or API billing status.")

if __name__ == "__main__":
    asyncio.run(diagnostic())
