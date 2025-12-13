from models import UsersBase
from aiogram.types import InlineKeyboardMarkup
from aiogram import Bot
import logging
import os


bot = Bot(os.getenv("BOT_TOKEN"))


async def start_spamming(
    user: UsersBase,
    message_text: str | None, 
    markup: InlineKeyboardMarkup | None
) -> bool:
    try:
        await bot.send_message(
            chat_id = user.chat_id,
            text = message_text,
            reply_markup = markup
        )

        return True
    except Exception as e:
        logging.error(f"message was not sent: {e}")
        return False