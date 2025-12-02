from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_playlists import PlaylistCallback
from models import PlaylistsBase



async def retreive_playlist(
    playlist_data: PlaylistsBase,
    limit: int = 6,
    offset: int = 0,
    track_offset: int = 0,
    track_limit: int = 6,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    start = track_offset*track_limit
    finish = start + track_limit

    for i, value in enumerate(playlist_data.songs[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.song_title}",
                callback_data = PlaylistCallback(
                    action = "audio",
                    playlist_id = playlist_data.id,
                    track_id = value.id,
                    limit = limit,
                    offset = offset,
                    track_offset = track_offset,
                    track_limit = track_limit,
                ).pack()
            )
        )

    kb.adjust(2)

    kb.row(
        InlineKeyboardButton(
            text = "Удалить плейлист",
            callback_data = PlaylistCallback(
                action = "delete",
                playlist_id = playlist_data.id,
                limit = limit,
                offset = offset
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Вернуться",
            callback_data = PlaylistCallback(
                action = "get",
                limit = limit,
                offset = offset
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