from utils.sql_requests.user_requests import UsersRequestsSQL
from utils.keyboards.menu_getter import get_menu
from .menu_btns.search.search_btn import search_btn_router
from .menu_btns.top.top_handler import tops_router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from views.menu_handlers.menu_btns.favorit.favorit_handler import favorit_router
from views.menu_handlers.admin_handlers.data_about_users.userdata_receive import get_data_router
from crude.crude_path import path_vibe_final
from views.menu_handlers.admin_handlers.send_messages.messaging import messaging_router
import asyncio
import logging


menu_router = Router()

menu_router.include_router(search_btn_router)
menu_router.include_router(tops_router)
menu_router.include_router(favorit_router)
menu_router.include_router(get_data_router)
menu_router.include_router(messaging_router)


@menu_router.message(Command("start"))
async def get_user_data(msg: Message):
    user = await UsersRequestsSQL.get_user_by_id(
        tg_id = msg.from_user.id
    )


    if not user:
        new_user_data = msg.from_user
        user = await UsersRequestsSQL.create_new_user(
            tg_id = new_user_data.id,
            first_name = new_user_data.first_name,
            last_name = new_user_data.last_name,
            username = new_user_data.username,
            chat_id = msg.chat.id
        )
    elif user:
        if not user.is_active:
            await UsersRequestsSQL.activate_deactivate_user_by_id(
                tg_id = msg.from_user.id,
                toggle_status = True
            )


    await msg.answer_animation(
        # caption = "Меню",
        animation = FSInputFile(path_vibe_final),
        reply_markup = await get_menu(user)
    )

