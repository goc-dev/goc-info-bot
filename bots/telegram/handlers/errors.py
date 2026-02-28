from aiogram import Router, types
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.error()
async def error_handler(event: types.ErrorEvent) -> None:
    """Global error handler to prevent bot crashes"""
    logger.error("❌ Error occurred while processing update:", exc_info=event.exception)