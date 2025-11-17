from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


tops_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "По жанрам",
                callback_data = "shutter"
            ),
            InlineKeyboardButton(
                text = "По странам",
                callback_data = "shutter"
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