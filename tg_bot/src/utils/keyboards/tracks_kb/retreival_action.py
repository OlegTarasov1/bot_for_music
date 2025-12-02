from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from settings.cache_settings import redis_client
import logging
from utils.api_integrations.sound_cloud_api.search import search_for_music
import json


async def retreival_action_choice(
    track_id: int,
    request: str,
    limit: int,
    offset: int
) -> InlineKeyboardMarkup:
    
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text = "Скачать",
            callback_data = MusicCallback(
                action = "download",
                limit=limit,
                request=request,
                offset=offset,
                track_id=track_id
            ).pack()
        )
    )
    kb.add(
        InlineKeyboardButton(
            text = "Назад",
            callback_data = MusicCallback(
                action = "get",
                offset = offset,
                limit = limit,
                request=request
            ).pack()
        )
    )
    kb.add(
        InlineKeyboardButton(
            text = "Добавить в плейлист",
            callback_data = MusicCallback(
                action = "add_pl",
                limit = limit,
                offset = offset,
                request = request,
                track_id=track_id
            ).pack()
        )
    )
    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()
