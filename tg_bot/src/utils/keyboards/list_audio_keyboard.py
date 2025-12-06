from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemas.cb_schemas.cb_list_music import MusicCallback
from settings.cache_settings import redis_client, redis_client_requests
from utils.tops.get_tops import get_top_by_country
from utils.api_integrations.sound_cloud_api.search import search_for_music
import logging
import json


async def list_music_kb(
    request: str,
    limit: int = 10,
    offset: int = 0
) -> InlineKeyboardMarkup:
    
    json_list = await redis_client.get(request)
    if json_list:
        json_list = json.loads(json_list)
    
    if not json_list:
        match request.startswith("top_"):
            case False:
                json_list = await search_for_music(
                    search_data=request
                )
                await redis_client.set(
                    request,
                    json.dumps(
                        json_list
                    ).encode("utf-8"),
                    ex = 60*60
                )
            case True:
                top_json = await get_top_by_country(
                    country = request[4:]
                )

                json_list = []
                for i in top_json.get("track", dict()):
                    if i.get("name", None):
                        track_data = await search_for_music(
                            search_data = i.get("name"),
                            max_results = 1
                        )
                        json_list.append(*track_data)

                if json_list:
                    await redis_client.set(
                        request,
                        json.dumps(json_list),
                        ex = 60*60*24
                    )

    kb = InlineKeyboardBuilder()

    start = limit*offset
    finish = limit*offset + limit

    for i, value in enumerate(json_list[start:finish]):
        kb.add(
            InlineKeyboardButton(
                text = f"{start + i + 1}. {value.get('title')}",
                callback_data = MusicCallback(
                    action = "retreive",
                    offset = offset,
                    limit = limit,
                    # request = request,
                    track_id = value.get('id')
                ).pack()
            )
        )
    kb = kb.adjust(2)

    nav_blk = []
    if start > 0:
        nav_blk.append(
            InlineKeyboardButton(
                text = "Назад",
                callback_data = MusicCallback(
                    action = "get",
                    offset = offset - 1,
                    limit = limit,
                    # request = request
                ).pack()
            )
        )
    if finish < len(json_list):
        nav_blk.append(
            InlineKeyboardButton(
                text = "Вперёд",
                callback_data = MusicCallback(
                    action = "get",
                    offset = offset + 1,
                    # request = request,
                    limit = limit
                ).pack()
            )
        )

    if nav_blk:
        kb.row(
            *nav_blk
        )

    kb.row(
        InlineKeyboardButton(
            text = "Меню",
            callback_data = "menu"
        )
    )

    return kb.as_markup()
    
