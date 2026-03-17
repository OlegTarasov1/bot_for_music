from utils.sql_requests.user_requests import UsersRequestsSQL
import logging
from settings.cache_settings import redis_client_sql
from aiogram.types import CallbackQuery
from utils.extra_funcs.utm_stats_retreive import retreive_utm_stats
from aiogram import Router, F
from datetime import datetime, timedelta
import json


get_data_router = Router()


@get_data_router.callback_query(F.data == "get_data_about_users")
async def get_users_data(
    cb: CallbackQuery
):
    response_text = f"Подписки:\n\n"
    unfollowed_users = 0
    subscribed_today = []

    # Получение пользователей (не админов)
    users_list = await UsersRequestsSQL.get_all_users()
    response_text += f"Всего пользователей (за всё время подписывалось): {len(users_list)}\n"

    # Получение из кэша пользователей, которые использовали бота недавно
    used_bot_not_long_ago = await redis_client_sql.keys(pattern = "user_*")
    response_text += f"Использовали бота недавно: {len(used_bot_not_long_ago)}\n"

    # Сборка пользователей сейчас подписаных
    response_text += f"Пользователей подписано сейчас: {len(users_list) - unfollowed_users}\n"

    # сборка пользователей, подписавшихся сегодня
    for i in users_list:
        if i.time_created.date() == datetime.today().date():
            subscribed_today.append(i)

    response_text += f"Подписалось сегодня: {len(subscribed_today)}\n"




    response_text += f"\nОтписки:\n\n"

    # Отписалось всего (не админов)
    for i in users_list:
        if not i.is_active:
            unfollowed_users += 1
    
    response_text += f"Всего пользователей (за всё время отписалось): {unfollowed_users}\n"

    # сборка списка отписавшихся 
    unsubscribed_today = 0
    for i in users_list:
        if i.is_active == False and i.activation_toggle_time.date() == datetime.now().date():
            unsubscribed_today += 1
    response_text += f"Отписалось сегодня: {unsubscribed_today}\n"

    week_ago = datetime.now() - timedelta(days=7)

    # Отписались за неделю
    # unsubscribed_within_a_week = 0
    unsubscribed_within_a_week_2 = sum(
        1
        for i in users_list
        if i.is_active == False
        and i.activation_toggle_time is not None
        and i.activation_toggle_time > week_ago
    )
    try:
        logging.warning(unsubscribed_within_a_week_2)
    except Exception as e:
        logging.warning(e)

    response_text += f"Отписок за неделю: {unsubscribed_within_a_week_2}"




    # сборка ютм статы и добавление её в сообщение
    utm_stats = await retreive_utm_stats()
    
    response_text += "\n\n" + "Статистика по трафику (UTM-метки):\n\n" + utm_stats

    await cb.message.answer(
        text = response_text
    )





# get_data_about_users