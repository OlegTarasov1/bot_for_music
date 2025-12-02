from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_playlists import PlaylistCallback
from models import PlaylistsBase


async def retreive_audio_data(
    playlist_id: int,
    track_id: int,
    limit: int = 6,
    offset: int = 0,
    track_offset: int = 0 ,
    track_limit: int = 6,
):
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text = "Скачать",
            callback_data = PlaylistCallback(
                action = "get_track",
                playlist_id = playlist_id,
                limit = limit,
                offset = offset,
                track_limit = track_limit,
                track_offset = track_offset,
                track_id = track_id
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Назад",
            callback_data = PlaylistCallback(
                action = "retreive",
                playlist_id = playlist_id,
                limit = limit,
                offset = offset,
                track_limit = track_limit,
                track_offset = track_offset
            ).pack()
        )
    )

    kb.row(
        InlineKeyboardButton(
            text = "Удалить из плейлиста",
            callback_data = PlaylistCallback(
                action = "del_conn",
                playlist_id = playlist_id,
                limit = limit,
                offset = offset,
                track_limit = track_limit,
                track_offset = track_offset,
                track_id = track_id
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