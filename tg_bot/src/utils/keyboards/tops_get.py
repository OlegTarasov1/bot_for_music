from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


tops_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "По жанрам",
                callback_data = "tops_by_genres"
            ),
            InlineKeyboardButton(
                text = "По странам",
                callback_data = "tops_by_countries"
            )
        ],
        [
            InlineKeyboardButton(
                text = "меню",
                callback_data = "menu"
            )
        ]
    ]
)