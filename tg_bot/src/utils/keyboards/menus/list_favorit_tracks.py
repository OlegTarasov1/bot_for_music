from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from models import SongsBase


async def list_favorit_tracks_kb(
    tracks_list: list[SongsBase],
    offset: int = 0,
    limit: int = 10
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = start + limit

    for i, value in enumerate(tracks_list[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.song_title}",
                callback_data = TrackCallbacks(
                    action = "retreive_fav",
                    limit = limit,
                    track_id = value.id,
                    offset = offset
                ).pack()
            )
        )

    kb.adjust(2)

    nav = []
    if start > 0:
        nav.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = TrackCallbacks(
                    action = "get_fav",
                    limit = limit,
                    offset = offset - 1
                ).pack()
            )
        )

    if finish < len(tracks_list):
        nav.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = TrackCallbacks(
                    action = "get_fav",
                    limit = limit,
                    offset = offset + 1
                ).pack()
            )
        )
    
    kb.row(*nav)
    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()

