from models.models import PlaylistsBase
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_playlists import PlaylistCallback
import logging


async def list_playlists_kb(
    playlists: list[PlaylistsBase],
    limit: int = 6,
    offset: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = limit * offset
    finish = start + limit

    if start > len(playlists) - 1:
        start -= limit
        finish -= limit
        
    for i, value in enumerate(playlists[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.title}",
                callback_data = PlaylistCallback(
                    action = "retreive",
                    limit = limit,
                    offset = offset,
                    playlist_id = value.id 
                ).pack()
            )
        )

    kb.add(
        InlineKeyboardButton(
            text = "добавить плейлист +",
            callback_data = "new_playlist"
        )
    )

    kb.adjust(1)

    nav_btns = []

    if start > 0:
        nav_btns.append(
            InlineKeyboardButton(
                text = "◀️ Назад",
                callback_data = PlaylistCallback(
                    action = "get",
                    limit = limit,
                    offset = offset - 1
                ).pack()
            )
        )

    if finish < len(playlists):
        nav_btns.append(
            InlineKeyboardButton(
                text = "Вперёд ▶️",
                callback_data = PlaylistCallback(
                    action = "get",
                    limit = limit,
                    offset = offset + 1
                ).pack()
            )
        )

    kb.row(*nav_btns)

    kb.row(
        InlineKeyboardButton(
            text = "🔙 Назад",
            callback_data = "menu"
        )
    )

    return kb.as_markup()
