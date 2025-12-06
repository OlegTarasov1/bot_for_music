from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks


user_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(
            text = "Поиск 🔍",
            callback_data = "handle_search"
        )],
        [InlineKeyboardButton(
            text = "Плейлисты 🎧",
            callback_data = "playlists"
        )],
        [InlineKeyboardButton(
            text = "Топы",
            callback_data = "tops"
        )],
        [InlineKeyboardButton(
            text = "Избранное",
            callback_data = TrackCallbacks(
                action = "get_fav"
            ).pack()
        )],
    ]
)



