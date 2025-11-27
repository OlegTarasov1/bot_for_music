from utils.sql_requests.user_requests import UsersRequestsSQL
from utils.keyboards.menu_getter import get_menu
from .menu_btns.search.search_btn import search_btn_router
from .menu_btns.top.top_handler import tops_router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
import asyncio
import logging

menu_router = Router()

menu_router.include_router(search_btn_router)
menu_router.include_router(tops_router)

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

    await msg.answer(
        text = "Меню",
        reply_markup = await get_menu(user)
    )

