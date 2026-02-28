from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo_message(message: Message) -> None:
    """Echo any other text message back to the user"""
    # Check if it's not a command (commands start with /)
    if not message.text.startswith('/'):
        await message.answer(f"📨 You said: {message.text}")
    # Commands will be handled by commands.py router