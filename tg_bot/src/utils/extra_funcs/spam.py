from models import UsersBase
from aiogram.types import InlineKeyboardMarkup
from aiogram import Bot
import logging
import os


bot = Bot(os.getenv("BOT_TOKEN"))


async def start_spamming(
    user: UsersBase,
    message_text: str | None, 
    media: str | None,
    markup: InlineKeyboardMarkup | None
) -> bool:
    try:
        if media:
            match media[:5]:
                case "video":
                    await bot.send_video(
                        chat_id = user.chat_id,
                        caption = message_text,
                        video = media.strip("video_"),
                        reply_markup = markup
                    )
                case "photo":
                    await bot.send_photo(
                        caption = message_text,
                        chat_id = user.chat_id,
                        photo = media.strip("photo_"),
                        reply_markup = markup
                    )
                case "anima":
                    await bot.send_animation(
                        chat_id = user.chat_id,
                        caption = message_text,
                        animation = media.strip("animation_"),
                        reply_markup = markup
                    )
                case _:
                    return False
                
            
            return True
        else:    
            await bot.send_message(
                chat_id = user.chat_id,
                text = message_text,
                reply_markup = markup
            )

        return True

    except Exception as e:
        logging.error(f"message was not sent: {e}")
        return False