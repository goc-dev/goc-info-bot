from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command"""
    await message.answer(
        "👋 Bot is running on BotHost.ru"
        "\n\n/help - Show available commands"
    )

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help command"""
    base_commands = (
        "📋 Available commands:"
        "\n/start - Start the bot"
        "\n/help - Show this help"
        "\n/ping - Simple health check"
    )
    if message.from_user.id in config.ADMIN_IDS:
        base_commands += "\n/admin - Show admin IDs (admin only)"
    base_commands += (
        "\n\nJust send any message and I'll echo it back!"
        "\n\nVersion: 0.1.4-2026-0314-0917"
    )
    await message.answer(base_commands)

@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    """Handle /ping command - simple health check"""
    await message.answer("🏓 Pong!")

@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    """Handle /admin command - show admin IDs"""
    if message.from_user.id not in config.ADMIN_IDS:
        await message.answer("⛔ You are not authorized to use this command.")
        return
    admin_ids = config.ADMIN_IDS
    if not admin_ids:
        await message.answer("No admin IDs configured.")
    else:
        ids_str = ", ".join(str(id) for id in admin_ids)
        await message.answer(f"Admin IDs: {ids_str}")