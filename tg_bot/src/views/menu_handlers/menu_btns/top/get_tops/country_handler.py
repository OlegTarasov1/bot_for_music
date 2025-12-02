from utils.api_integrations.sound_cloud_api.search import search_for_music
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback
from utils.keyboards.list_audio_keyboard import list_music_kb
from utils.tops.get_tops import get_top_by_country
from settings.cache_settings import redis_client
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
import logging
from crude.crude_path import path_vibe_final
import json


country_getting_router = Router()


@country_getting_router.callback_query(CountriesTopsCallback.filter(F.country.startswith("top_")))
async def country_top_handler(
    cb: CallbackQuery,
    callback_data: CountriesTopsCallback
):
    top = await redis_client.get(callback_data.country)

    logging.warning(top)

    if not top:
        logging.warning("there was nothing in cache")
        country = callback_data.country[4:]
        top_json = await get_top_by_country(
            country = country
        )


        new_top = []
        for i in top_json.get("track", dict()):
            if i.get("name", None):
                track_data = await search_for_music(
                    search_data = i.get("name"),
                    max_results = 1
                )
                new_top.append(*track_data)


        if new_top:
            await redis_client.set(
                callback_data.country,
                json.dumps(new_top),
                ex = 60*60
            )

        logging.warning(callback_data.country)

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Введите:",
        reply_markup = await list_music_kb(
            request = callback_data.country
        )
    ) 

        

        
