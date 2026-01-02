from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_list_music import MusicCallback


async def retreive_favorit_track_kb(
    track_id: int,
    limit: int = 6,
    offset: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text = "Скачать 📥",
            callback_data = MusicCallback(
                action = "download",
                track_id = track_id
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Назад ↩️",
            callback_data = TrackCallbacks(
                action = "get_fav",
                limit = limit,
                offset = offset
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Удалить из избранных 🗑️",
            callback_data = TrackCallbacks(
                action = "del_fav",
                track_id=track_id,
                limit = limit,
                offset = offset
            ).pack()
        )
    )

    kb.row(
        InlineKeyboardButton(
            text = "🔙 Назад",
            callback_data = "menu"
        )
    )

    return kb.as_markup()