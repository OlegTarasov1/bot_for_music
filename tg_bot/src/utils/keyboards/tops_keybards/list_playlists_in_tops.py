from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from schemas.cb_schemas.cb_list_music import MusicCallback
from models import PlaylistsBase
import logging



async def list_playlists(
    playlists: list[PlaylistsBase],
    track_id: int,
    limit: int = 6,
    offset: int = 0,
    offset_pl: int = 0,
    limit_pl: int = 6,
    genre: str | None = None
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = start + limit

    for i, value in enumerate(playlists[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.title}",
                callback_data = GenresTopsCallback(
                    action = "add_pl",
                    limit = limit,
                    offset = offset,
                    offset_pl = offset_pl,
                    limit_pl = limit_pl,
                    track_id = track_id,
                    playlist_id = value.id,
                    genre = genre
                ).pack()
            )
        )

    kb.adjust(1)

    nav = []

    if start > 0:
        nav.append(
            InlineKeyboardButton(
                text = "◀️ Назад",
                callback_data = GenresTopsCallback(
                    action = "list_pl",
                    limit = limit,
                    offset = offset,
                    offset_pl = offset_pl,
                    limit_pl = limit_pl,
                    track_id = track_id,
                    genre = genre
                ).pack()
            )
        )

    if finish < len(playlists):
        nav.append(
            InlineKeyboardButton(
                text = "Вперёд ▶️",
                callback_data = GenresTopsCallback(
                    action = "list_pl",
                    limit = limit,
                    offset = offset,
                    offset_pl = offset_pl,
                    limit_pl = limit_pl,
                    track_id = track_id,
                    genre = genre
                ).pack()
            )
        )
    
    kb.row(*nav)

    kb.row(
        InlineKeyboardButton(
            text = "Вернуться ↩️",
            callback_data = GenresTopsCallback(
                action = "retreive_track",
                limit = limit,
                offset = offset,
                offset_pl = offset_pl,
                limit_pl = limit_pl,
                track_id = track_id,
                genre = genre
            ).pack()
        )
    )
    kb.row(
        InlineKeyboardButton(
            text = "Меню 📑",
            callback_data = "menu"
        )
    )

    return kb.as_markup()