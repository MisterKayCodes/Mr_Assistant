import asyncio
import sys

# THE ORCHESTRATOR: The Conductor of the Mr. Assistant Symphony.
# Rules: Senior-level assembly, zero logic leaks, safe shutdown.

async def main():
    """
    The Heart of the Bot.
    SENIOR REFINE: Simplified stable initialization for Windows.
    """
    # 1. Lazy Imports (Directly before use to avoid import deadlocks)
    from aiogram import Bot, Dispatcher
    from config import config
    from app.bot.handlers import router as main_router
    from app.bot.middlewares.logging import LoggingMiddleware
    from app.utils.logger import logger
    from app.services.gpt import gpt_service

    print("BOT HEART STRIKING...", flush=True)

    # Ensure directories are ready
    config.ensure_directories()

    # 2. Standard Bot Initialization (Let aiogram manage the session)
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    try:
        # 3. PULSE CHECK: Verify GPT Connectivity
        if await gpt_service.health_check():
            print("[OK] Intelligence Verified: GPT-4o-mini is responsive.", flush=True)
            logger.info("STARTUP: GPT Service is online.")
        else:
            print("[!] Intelligence Offline: Entering Text-Only Limp Mode.", flush=True)
            logger.warning("STARTUP: GPT Service failed health check. Intelligence is offline.")

        # 4. Connection Check (Telegram)
        try:
            bot_user = await asyncio.wait_for(bot.get_me(), timeout=10.0)
            logger.info(f"STARTUP: {bot_user.full_name} is online! (@{bot_user.username})")
        except Exception:
            logger.warning("WARNING: Initial connection check skipped. Entering polling...")

        # 5. Register Bouncer & Routers
        dp.update.middleware(LoggingMiddleware())
        dp.include_router(main_router)

        # 6. Start Polling
        logger.info("INIT: Polling logic activated.")
        print(">>> DISPATCHER ACTIVE: BOT IS LISTENING...", flush=True)
        await dp.start_polling(bot, skip_updates=True)

    except Exception as e:
        logger.critical(f"CRASH: Bot loop failure: {e}")
    finally:
        # 7. Clean Exit
        await bot.session.close()
        logger.info("EXIT: Heart stopped safely.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except Exception as e:
        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger(__name__).critical(f"FATAL: Uncaught error: {e}")
        sys.exit(1)
