from utils.keyboards.menus.user_menu import user_menu
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


admin_menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "Данные о пользователях",
                callback_data = "get_data_about_users"
            )
        ],
        [
            InlineKeyboardButton(
                text = "Массовая рассылка",
                callback_data = "send_messages"
            )
        ],
        *user_menu.inline_keyboard
    ]
)



