import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get bot token from environment variable (set in BotHost.ru admin panel)
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    error_msg = "No API_TOKEN found in environment variables"
    logging.error(error_msg)
    raise ValueError(error_msg)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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

@dp.message()
async def echo_message(message: Message) -> None:
    """Echo any other message"""
    await message.answer(f"📨 You said: {message.text}")

async def on_startup() -> None:
    """Actions to perform on startup"""
    me = await bot.me()
    logging.info(f"Bot @{me.username} (ID: {me.id}) started successfully!")
    logging.info(f"BotHost.ru deployment ready")

async def on_shutdown() -> None:
    """Actions to perform on shutdown"""
    logging.info("Bot shutting down...")

async def main() -> None:
    """Main function"""
    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())