from utils.sql_requests.user_requests import UsersRequestsSQL
import logging


async def retreive_utm_stats() -> str:
    """Получение ютм данных в текстовом формате"""
    stats_data = await UsersRequestsSQL.retreive_utm_user_data()

    response_list = []

    logging.warning(stats_data)

    for i in stats_data:
        if i.get("source") is None:
            response_list.append(f"Основная ссылка: {i.get('source_count')}")
        else:
            response_list.append(f"{i.get('source')}: {i.get('source_count')}")

    return "\n".join(response_list)