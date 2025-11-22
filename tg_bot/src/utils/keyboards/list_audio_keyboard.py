from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from settings.cache_settings import redis_client
import logging
from utils.api_integrations.sound_cloud_api.search import search_for_music
import json


async def list_music_kb(
    request: str,
    limit: int = 10,
    offset: int = 0
) -> InlineKeyboardMarkup:

    json_list = await redis_client.get(request)
    if json_list:
        json_list = json.loads(json_list)
    
    if not json_list:
        json_list = await search_for_music(request)
        await redis_client.set(request, json.dumps(json_list).encode("utf-8"), ex = 60*60)

    logging.warning(json_list[0])

    kb = InlineKeyboardBuilder()

    start = limit*offset
    finish = limit*offset + limit

    for i, value in enumerate(json_list[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.get('title')}",
                callback_data = MusicCallback(
                    action = "retreive",
                    offset = offset,
                    limit = limit,
                    request = request,
                    track_id = value.get('id')
                ).pack()
            )
        )
    if start > 0:
        kb.add(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = MusicCallback(
                    action = "get",
                    offset = offset - 1,
                    limit = limit,
                    request = request
                ).pack()
            )
        )
    if finish < len(json_list):
        kb.add(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = MusicCallback(
                    action = "get",
                    offset = offset + 1,
                    request = request,
                    limit = limit
                ).pack()
            )
        )
        kb = kb.adjust(2)

    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()
    
