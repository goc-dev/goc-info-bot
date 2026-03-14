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
        "\n\nVersion: 0.1.5-2026-0314-2318"
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
        lines = []
        for uid in admin_ids:
            username = ''
            try:
                chat = await message.bot.get_chat(uid)
                username = f"(@{chat.username})" if chat.username else "(no username)"
                #lines.append(f"- {uid} {username}")
            except Exception:
                username = "(not available)"
            lines.append(f"- {uid} {username}")
        response = "Admin IDs:\n" + "\n".join(lines)
        await message.answer(response)