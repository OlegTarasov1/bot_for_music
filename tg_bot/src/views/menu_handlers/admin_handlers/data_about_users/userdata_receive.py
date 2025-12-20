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
    # Получение пользователей (не админов)
    users_list = await UsersRequestsSQL.get_all_users()
    response_text = f"Всего пользователей (за всё время подписывалось): {len(users_list)}\n"

    # Отписалось всего (не админов)
    unfollowed_users = 0
    for i in users_list:
        if not i.is_active:
            unfollowed_users += 1
    
    response_text += f"Всего пользователей (за всё время отписалось): {unfollowed_users}\n"

    # Получение из кэша пользователей, которые использовали бота недавно
    used_bot_not_long_ago = await redis_client_sql.keys(pattern = "user_*")
    response_text += f"Использовали бота недавно: {len(used_bot_not_long_ago)}\n"

    # сборка пользователей, подписавшихся сегодня
    subscribed_today = []
    for i in users_list:
        if i.time_created.date() == datetime.today().date():
            subscribed_today.append(i)

    response_text += f"Подписалось сегодня: {len(subscribed_today)}\n"

    # сборка списка отписавшихся 
    unsubscribed_today = 0
    for i in users_list:
        if i.is_active == False and i.activation_toggle_time.date() == datetime.now().date():
            unsubscribed_today += 1

    response_text += f"Отписалось сегодня: {unsubscribed_today}"

    await cb.message.answer(
        text = response_text
    )





# get_data_about_users