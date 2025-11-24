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
                country = "top_usa"
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇺🇦",
            callback_data = CountriesTopsCallback(
                country = "top_ukraine"
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇷🇺",
            callback_data = CountriesTopsCallback(
                country = "top_russia"
            ).pack()
        ),
        InlineKeyboardButton(
            text = "spain",
            callback_data = CountriesTopsCallback(
                country = "top_spain"
            ).pack()
        ),
        InlineKeyboardButton(
            text = "🇰🇿",
            callback_data = "top_Kazachstan"
        ),
        InlineKeyboardButton(
            text = "🇫🇷",
            callback_data = "top_France"
        )
    )

    kb.adjust(3)
    
    kb.row(InlineKeyboardButton(
        text = "меню",
        callback_data = "menu"
    ))

    return kb.as_markup()