import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# --- LOGGING CONFIGURATION (essential for debugging on hosting) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- GET BOT TOKEN FROM ENVIRONMENT VARIABLES ---
# BotHost.ru sets API_TOKEN in the OS environment via admin panel
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    logger.error("CRITICAL ERROR: API_TOKEN not found in environment variables!")
    raise ValueError("API_TOKEN environment variable is required")

# --- INITIALIZE BOT AND DISPATCHER ---
# DefaultBotProperties sets default parameters for all messages (like parse mode)
bot = Bot(
    token=API_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- COMMAND HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command"""
    await message.answer(
        "👋 Hello! I'm your bot running on BotHost.ru\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help command"""
    await message.answer(
        "📋 Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n\n"
        "Just send any message and I'll echo it back!"
    )

@dp.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    """Handle /ping command - simple health check"""
    await message.answer("🏓 Pong!")

# --- ECHO HANDLER (for all non-command text messages) ---
@dp.message()
async def echo_message(message: Message) -> None:
    """Echo any other text message back to the user"""
    await message.answer(f"📨 You said: {message.text}")

# --- ERROR HANDLER (catches all exceptions in handlers) ---
@dp.error()
async def error_handler(event: types.ErrorEvent) -> None:
    """Global error handler to prevent bot crashes"""
    logger.error("Error occurred while processing update:", exc_info=event.exception)

# --- STARTUP FUNCTION (runs once when bot starts) ---
async def on_startup() -> None:
    """Actions to perform when bot starts"""
    try:
        # Get bot information from Telegram API
        me = await bot.me()
        logger.info(f"Bot @{me.username} (ID: {me.id}) is starting...")

        # CRITICAL: Clear any existing webhook
        # This ensures polling mode works correctly
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            logger.warning(f"Active webhook found: {webhook_info.url}. Deleting it...")
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook successfully deleted.")
        else:
            logger.info("No active webhooks found. Polling mode is safe.")

        logger.info("Bot is ready and waiting for messages!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise  # Re-raise to prevent bot from starting with errors

# --- SHUTDOWN FUNCTION (runs once when bot stops) ---
async def on_shutdown() -> None:
    """Actions to perform when bot stops"""
    logger.info("Bot is shutting down...")
    await bot.session.close()
    logger.info("Bot session closed.")

# --- MAIN FUNCTION ---
async def main() -> None:
    """Main entry point for the bot"""
    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling
    # allowed_updates=['message'] means we only receive message updates
    # This reduces bandwidth and processing
    await dp.start_polling(
        bot, 
        allowed_updates=['message'],
        skip_updates=True  # Skip pending updates from when bot was offline
    )

# --- ENTRY POINT ---
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually by keyboard interrupt.")
    except SystemExit:
        logger.info("Bot stopped by system exit.")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)