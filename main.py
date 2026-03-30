import asyncio
import sys
from aiogram import Bot, Dispatcher
from config import config
from app.bot.handlers import router as main_router
from app.bot.middlewares.logging import LoggingMiddleware
from app.utils.logger import logger

# THE ORCHESTRATOR: The Conductor of the Mr. Assistant Symphony.
# Rules: Senior-level assembly, zero logic leaks, safe shutdown.

async def main():
    # 1. Initialize Bot and Dispatcher
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    # 2. The "Shadow" Logger (Rule 16: Security & Safety)
    # Catching if we've loaded the wrong token before we do anything else.
    try:
        bot_user = await bot.get_me()
        logger.info(f"🚀 {bot_user.full_name} is coming online! (@{bot_user.username})")
    except Exception as e:
        logger.critical(f"❌ Failed to fetch bot info. Check your BOT_TOKEN! Error: {e}")
        return

    # 3. Register Middleware (The Bouncer)
    dp.update.middleware(LoggingMiddleware())

    # 4. Register Routers (The Orchestrated List)
    dp.include_router(main_router)

    # 5. Assembly Complete. Start Polling.
    logger.info("📡 Mr. Assistant Dispatcher initialized. Starting polling...")
    
    try:
        # We skip updates that happened while the bot was offline to avoid "Spam Storms"
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.critical(f"❌ Bot Polling crashed: {e}", exc_info=True)
    finally:
        # SENIOR REFINE: The "Clean Exit" Rule.
        # Closing the bot session ensures resources are freed safely.
        await bot.session.close()
        logger.info("🧠 Memory layer safely detached.")
        logger.info("💤 Mr. Assistant is going to sleep. Goodbye.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # We don't log a stack trace for Ctrl+C, just a clean exit.
        logger.info("Keyboard interrupt received. Exiting gracefully...")
        sys.exit(0)
