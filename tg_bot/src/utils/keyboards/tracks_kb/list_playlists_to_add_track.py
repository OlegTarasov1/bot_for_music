from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from models import PlaylistsBase


async def list_playlists_to_add_track(
    playlists: list[PlaylistsBase],
    track_id: int,
    request: str, 
    limit: int = 6,
    offset: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = offset * limit
    finish = start + limit

    for i, value in enumerate(playlists[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.title}",
                callback_data = TrackCallbacks(
                    action = "add",
                    track_id = track_id,
                    playlist_id = value.id,
                    request = request
                ).pack()
            )
        )

    kb.adjust(1)
    nav_btns = []

    if start > 0:
        nav_btns.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = TrackCallbacks(
                    action = "get",
                    track_id = track_id,
                    offset = offset - 1,
                    limit = limit,
                    request = request
                )
            )
        )

    if finish < len(playlists):
        nav_btns.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = TrackCallbacks(
                    action = "get",
                    track_id = track_id,
                    offset = offset + 1,
                    request=request,
                    limit = limit
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
