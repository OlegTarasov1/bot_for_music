from settings.cache_settings import redis_client_names



# функция для установки в кэш текстов запросов, ассоциированных с сообщением

async def set_name_in_cache(
    user_id: int,
    msg_id: int,
    name: str
) -> None:
    await redis_client_names.set(
        f"{user_id}:{msg_id}",
        str(name),
        ex = 60 * 60 * 24 * 80
    )


# Функция для получения из кэша текста запроса по message_id и user_id 

async def retreive_name_from_cache(
    user_id: int,
    msg_id: int
) -> str:
    response = await redis_client_names.get(
        f"{user_id}:{msg_id}"
    )

    return str(response)


