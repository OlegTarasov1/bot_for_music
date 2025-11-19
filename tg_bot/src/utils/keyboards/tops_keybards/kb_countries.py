from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.models import UsersBase
import logging


async def get_kb_for_tops_by_countries() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text = "меню",
        callback_data = "menu"
    ))

    return kb.as_markup()