from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def link_received_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(
        InlineKeyboardButton(
            text = "Скачать mp3 📥",
            callback_data = "get_audio"
        ),
        InlineKeyboardButton(
            text = "Скачать используемый трек 🎵",
            callback_data = "extract_audio"
        )
    )
    kb.row(
        InlineKeyboardButton(
            text = "🔙 Назад",
            callback_data = "menu"
        )
    )

    return kb.as_markup()