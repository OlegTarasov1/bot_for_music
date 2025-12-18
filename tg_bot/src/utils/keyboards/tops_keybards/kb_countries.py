from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback
from models.models import UsersBase
import logging


async def get_kb_for_tops_by_countries() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text = "🇺🇸",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "united states",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇺🇦",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "ukraine",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇷🇺",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "russian federation",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇪🇸",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "spain",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇰🇿",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country="kazakhstan",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇫🇷",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "france",
                limit = 10,
                offset = 0
            ).pack()
        ),
        # InlineKeyboardButton(
        #     text = "🇸🇪",
        #     callback_data = CountriesTopsCallback(
        #         action = "get_c_top",
        #         country = "sweden",
        #         limit = 10,
        #         offset = 0
        #     ).pack()
        # ),
        InlineKeyboardButton(
            text = "🇮🇳",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "india",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇲🇽",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "mexico",
                limit = 10,
                offset = 0
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇯🇵",
            callback_data = CountriesTopsCallback(
                action = "get_c_top",
                country = "japan",
                limit = 10,
                offset = 0
            ).pack()
        )

    )

    kb.adjust(3)
    
    kb.row(InlineKeyboardButton(
        text = "меню 📑",
        callback_data = "menu"
    ))

    return kb.as_markup()