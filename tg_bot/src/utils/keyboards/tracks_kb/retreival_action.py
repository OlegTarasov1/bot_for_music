from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from settings.cache_settings import redis_client
import logging
from utils.api_integrations.sound_cloud_api.search import search_for_music
import json


async def retreival_action_choice(
    track_id: int,
    limit: int,
    offset: int,
    *args,
    **kwargs
) -> InlineKeyboardMarkup:
    
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text = "Скачать 📥",
            callback_data = MusicCallback(
                action = "download",
                limit=limit,
                # request=request,
                offset=offset,
                track_id=track_id
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Вернуться ↩️",
            callback_data = MusicCallback(
                action = "get",
                offset = offset,
                limit = limit,
                # request=request
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Добавить в плейлист 🎧",
            callback_data = MusicCallback(
                action = "add_pl",
                limit = limit,
                offset = offset,
                # request = request,
                track_id=track_id
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Добавить в избранное 💖",
            callback_data = TrackCallbacks(
                action = "add_fav",
                track_id = track_id
            ).pack()
        )
    )

    kb.adjust(2)

    kb.row(
        InlineKeyboardButton(
            text = "🔙 Назад",
            callback_data = "menu"
        )
    )

    return kb.as_markup()
