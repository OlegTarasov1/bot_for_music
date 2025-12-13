from utils.sql_requests.user_requests import UsersRequestsSQL
from settings.cache_settings import redis_client_sql
from aiogram.types import CallbackQuery
from aiogram import Router, F
from datetime import datetime
import json


get_data_router = Router()


@get_data_router.callback_query(F.data == "get_data_about_users")
async def get_users_data(
    cb: CallbackQuery
):
    # Получение пользователей (не админов) # noqa
    users_list = await UsersRequestsSQL.get_all_users()
    response_text = f"Всего пользователей: {len(users_list)}\n"


    # Получение из кэша пользователей, которые использовали бота недавно #noqa
    used_bot_not_long_ago = await redis_client_sql.keys(pattern = "user_*")
    # used_bot_not_long_ago = json.loads(used_bot_not_long_ago)
    response_text += f"Использовали бота недавно: {len(used_bot_not_long_ago)}\n"


    # сборка пользователей, подписавшихся сегодня # noqa
    subscribed_today = []
    for i in users_list:
        if i.time_created.date() == datetime.today().date():
            subscribed_today.append(i)

    response_text += f"Подписалось сегодня: {len(subscribed_today)}\n"


    # Получение списка отписавшихся из redis # noqa
    unsubscribed_today = await redis_client_sql.keys(pattern = "unsubscribed_*")
    # unsubscribed_today = json.loads(unsubscribed_today)
    response_text += f"Отписалось сегодня: {len(unsubscribed_today)}"


    await cb.message.answer(
        text = response_text
    )





# get_data_about_users