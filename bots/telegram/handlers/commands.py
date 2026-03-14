from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command"""
    await message.answer(
        "👋 Bot is running on BotHost.ru"
        "\n\nAvailable commands:"
        "\n/start - Start the bot"
        "\n/help - Show this help"
        "\n/ping - Simple health check"
    )

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help command"""
    await message.answer(
        "📋 Available commands:"
        "\n/start - Start the bot"
        "\n/help - Show this help"
        "\n\nJust send any message and I'll echo it back!"
        "\n\nVersion: 0.1.3-2026-0314-0824"
    )

@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    """Handle /ping command - simple health check"""
    await message.answer("🏓 Pong!")