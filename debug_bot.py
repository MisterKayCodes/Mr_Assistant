import asyncio
from aiogram import Bot
import os
from dotenv import load_dotenv

async def debug_bot():
    print("[...] Reading .env...")
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("[!] ERROR: No BOT_TOKEN found in .env")
        return

    print(f"[...] Attempting bot.get_me() with token ending in ...{token[-5:]}")
    bot = Bot(token=token)
    
    try:
        # Use a timeout to ensure we don't hang forever
        user = await asyncio.wait_for(bot.get_me(), timeout=10)
        print(f"[OK] Bot is alive: {user.full_name} (@{user.username})")
    except asyncio.TimeoutError:
        print("[!] ERROR: Connection timeout! Is your internet working? Is Telegram blocked?")
    except Exception as e:
        print(f"[!] ERROR: Failed to fetch bot info: {e}")
    finally:
        await bot.session.close()
        print("[...] Session closed.")

if __name__ == "__main__":
    asyncio.run(debug_bot())
