from models import UsersBase
from aiogram.types import InlineKeyboardMarkup, MessageEntity
from aiogram import Bot
import logging
import os 

bot = Bot(os.getenv("BOT_TOKEN"))


async def start_spamming(
    user: UsersBase,
    message_text: str | None = None, 
    media: str | None = None,
    entities: list[MessageEntity] | None = None,
    markup: InlineKeyboardMarkup | None = None
) -> bool:
    try:
        logging.warning(entities)
        if media:
            match media[:5]:
                case "video":
                    await bot.send_video(
                        caption_entities = entities,
                        chat_id = user.chat_id,
                        caption = message_text,
                        video = media.strip("video_"),
                        reply_markup = markup
                    )
                case "photo":
                    await bot.send_photo(
                        caption_entities = entities,
                        caption = message_text,
                        chat_id = user.chat_id,
                        photo = media.strip("photo_"),
                        reply_markup = markup
                    )
                case "anima":
                    await bot.send_animation(
                        caption_entities = entities,
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
                entities = entities,
                chat_id = user.chat_id,
                text = message_text,
                reply_markup = markup
            )

        return True

    except Exception as e:
        logging.error(f"message was not sent: {e}")
        return False