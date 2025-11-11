from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

user_router = Router()

@user_router.message(Command("start"))
async def get_user_data(msg: Message):
    user = await UsersRequestsSQL.get_user_by_id(
        tg_id = msg.from_user.id
    )
    if user:
        await msg.answer("the user is present in the database")
    else:
        new_user_data = msg.from_user
        new_user = await UsersRequestsSQL.create_new_user(
            tg_id = new_user_data.id,
            first_name = new_user_data.first_name,
            last_name = new_user_data.last_name,
            username = new_user_data.username,
            chat_id = msg.chat.id
        )
        await msg.answer("the user is created and now present in the database")