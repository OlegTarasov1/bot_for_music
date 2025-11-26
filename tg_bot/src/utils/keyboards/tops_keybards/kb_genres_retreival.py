from utils.api_integrations.sound_cloud_api.search import search_for_music_by_tag
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
from settings.cache_settings import redis_client
from models.models import UsersBase
import json
import logging



async def retreive_genre(
    genre: str,
    offset: int = 0,
    limit: int = 10
) -> InlineKeyboardMarkup:

    logging.warning(genre)

    json_data = await redis_client.get(genre)

    if json_data:
        json_data = json.loads(json_data)
    else:
        json_data = await search_for_music_by_tag(
            search_data = genre[4:].replace("_", " ")
        )
        await redis_client.set(
            genre,
            json.dumps(json_data),
            ex = 60*60*24
        )

    print(json_data)

    start = offset * limit
    finish = start + limit

    kb = InlineKeyboardBuilder()

    for i, value in enumerate(json_data[start:finish]):
        logging.warning(value.get("id"))
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.get('title')}",
                callback_data = GenresTopsCallback(
                    action = "retreive_track",
                    offset = offset,
                    limit = limit,
                    genre = genre,
                    track_id = value.get('id')
                ).pack()
            )
        )
    kb = kb.adjust(2)
    
    nav_blk = []
    if start > 0:
        nav_blk.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = GenresTopsCallback(
                    action = "retreive",
                    offset = offset - 1,
                    limit = limit,
                    genre = genre
                ).pack()
            )
        )
    if finish < len(json_data):
        nav_blk.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = GenresTopsCallback(
                    action = "retreive",
                    offset = offset + 1,
                    genre = genre,
                    limit = limit
                ).pack()
            )
        )

    if nav_blk:
        kb.row(
            *nav_blk
        )

    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()

    