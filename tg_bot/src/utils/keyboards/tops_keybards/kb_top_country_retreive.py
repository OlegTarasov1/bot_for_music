from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback
from schemas.cb_schemas.cb_list_music import MusicCallback


async def kb_track_for_country_retreival(
    track_id: int,
    country: str,
    limit: int = 10,
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
            text = "Вернуться ↩️",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                track_id = track_id,
                limit = limit,
                offset = offset,
                limit_pl = 10,
                country = country,
                offset_pl = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Добавить в избранное ❤️",
            callback_data = TrackCallbacks(
                action = "add_fav",
                track_id = track_id
            ).pack()
        ),
        InlineKeyboardButton(
            text = "Добавить в плейлист 🎧",
            callback_data = CountriesTopsCallback(
                action = "choose_pl",
                track_id = track_id,
                limit = limit,
                offset = offset,
                limit_pl = 10,
                country = country,
                offset_pl = 0
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
