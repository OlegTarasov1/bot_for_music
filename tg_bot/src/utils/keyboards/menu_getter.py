from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from .menus.admin_menue import admin_menu
from .menus.user_menu import user_menu
from models.models import UsersBase
import logging


async def get_menu(
    user: UsersBase | int
) -> InlineKeyboardMarkup | None:
    """Функция получения клавиатуры меню"""
    if isinstance(user, int):
        user = await UsersRequestsSQL.get_user_by_id(user)
        logging.warning("user collected for the menu")
    if user:
        match user.is_admin:
            case True:
                return admin_menu
            case False:
                return user_menu
    else:
        logging.warning(
            "user tried to use the bot without being registered."
        )
        return user_menu
    
menu_r_mk = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(
                text = "Главное меню 📋"
            )
        ]
    ],
    resize_keyboard = True
)