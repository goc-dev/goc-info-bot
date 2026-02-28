import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to Python path (ensures imports work from anywhere)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
#from dotenv import load_dotenv

# Import routers from handlers
from bots.telegram.handlers.commands import router as commands_router
from bots.telegram.handlers.echo import router as echo_router
from bots.telegram.handlers.errors import router as errors_router

# Load environment variables
#load_dotenv()

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- GET BOT TOKEN FROM ENVIRONMENT VARIABLES ---
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logger.error("CRITICAL ERROR: API_TOKEN not found in environment variables!")
    raise ValueError("API_TOKEN environment variable is required")

# --- INITIALIZE BOT AND DISPATCHER ---
bot = Bot(
    token=API_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- INCLUDE ROUTERS (this replaces register_handlers) ---
dp.include_router(commands_router)
dp.include_router(echo_router)
dp.include_router(errors_router)
logger.info("✅ All routers included successfully")

# --- STARTUP FUNCTION ---
async def on_startup() -> None:
    """Actions to perform when bot starts"""
    try:
        me = await bot.me()
        logger.info(f"🤖 Bot @{me.username} (ID: {me.id}) is starting...")

        # Clear any existing webhook
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            logger.warning(f"⚠️ Active webhook found: {webhook_info.url}. Deleting it...")
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("✅ Webhook successfully deleted.")
        else:
            logger.info("✅ No active webhooks found. Polling mode is safe.")

        logger.info("🚀 Bot is ready and waiting for messages!")
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}", exc_info=True)
        raise

# --- SHUTDOWN FUNCTION ---
async def on_shutdown() -> None:
    """Actions to perform when bot stops"""
    logger.info("🛑 Bot is shutting down...")
    await bot.session.close()
    logger.info("✅ Bot session closed.")

# --- MAIN FUNCTION ---
async def main() -> None:
    """Main entry point for the bot"""
    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling
    await dp.start_polling(
        bot, 
        allowed_updates=['message'],
        skip_updates=True
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped manually by keyboard interrupt.")
    except SystemExit:
        logger.info("👋 Bot stopped by system exit.")
    except Exception as e:
        logger.critical(f"💥 Critical error: {e}", exc_info=True)