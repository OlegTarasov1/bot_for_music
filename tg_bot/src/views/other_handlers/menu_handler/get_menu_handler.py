from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.keyboards.menu_getter import get_menu

get_menu_router = Router()


@get_menu_router.callback_query(F.data == "menu")
async def return_menu(cb: CallbackQuery):
    await cb.message.edit_text(
        text = "меню:",
        reply_markup = await get_menu(cb.from_user.id)
    )

