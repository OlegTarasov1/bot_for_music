from utils.api_integrations.sound_cloud_api.search import search_for_music, get_soundcloud_track_by_id
from utils.keyboards.tops_keybards.kb_top_by_country import list_top_for_country_kb
from utils.keyboards.tops_keybards.kb_top_country_retreive import kb_track_for_country_retreival
from utils.keyboards.tops_keybards.kb_pl_choose import kb_choose_pl
from schemas.cb_schemas.cb_tops_countries import CountriesTopsCallback
from utils.keyboards.list_audio_keyboard import list_music_kb
from utils.tops.get_tops import get_top_by_country
from settings.cache_settings import redis_client_top, redis_client
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
from utils.sql_requests.track_requests import TrackRequestsSQL
import logging
from crude.crude_path import path_vibe_final
import json


country_getting_router = Router()


# Обработка получения топа треков по стране

@country_getting_router.callback_query(CountriesTopsCallback.filter(F.action == "get_c_top"))
async def country_top_handler(
    cb: CallbackQuery,
    callback_data: CountriesTopsCallback
):
    top_country_data = await redis_client_top.get(callback_data.country)
    if top_country_data:
        top_countries_json = json.loads(top_country_data)
    else:
        top = await get_top_by_country(country = callback_data.country)
        top_countries_json = []
        for i in top.get("track", dict()):
            logging.warning(f"last_fm: {i}")
            if i.get("name", None):
                track_data = await search_for_music(
                    search_data = i.get("name"),
                    max_results = 1
                )
                track_data = track_data[0]
                
                await redis_client_top.set(
                    f"track_{track_data.get('id', 'null')}",
                    json.dumps(track_data),
                    ex = 60 * 60 * 24 * 2
                )
                top_countries_json.append(track_data)

        await redis_client_top.set(
            callback_data.country,
            json.dumps(top_countries_json),
            ex = 60 * 60 * 24
        )

    await cb.message.edit_caption(
        reply_markup = await list_top_for_country_kb(
            country_name = callback_data.country,
            limit = callback_data.limit,
            offset = callback_data.offset,
            top_countries_json = top_countries_json
        )
    )


# Обработка получения трека из топа

@country_getting_router.callback_query(CountriesTopsCallback.filter(F.action == "retreive"))
async def track_retreival(
    cb: CallbackQuery,
    callback_data: CountriesTopsCallback
):
    logging.warning("retreival handled")
    track_data = await redis_client_top.get(f"track_{callback_data.track_id}")
    if track_data:
        track_data = json.loads(track_data)
    else:
        track_data = await get_soundcloud_track_by_id(
            track_id = callback_data.track_id
        )
        if isinstance(track_data, list):
            track_data = track_data[0]
        
        await redis_client_top.set(
            f"track_{track_data.get('id', 'null')}",
            json.dumps(track_data),
            ex = 60 * 60 * 24
        )


    await cb.message.edit_caption(
        caption = track_data.get("title", "title"),
        reply_markup = await kb_track_for_country_retreival(
            track_id = callback_data.track_id,
            country = callback_data.country,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Обработка выбора плейлиста для добавления трека из топов.

@country_getting_router.callback_query(CountriesTopsCallback.filter(F.action == "choose_pl"))
async def choose_playlist_to_add_track_to(
    cb: CallbackQuery,
    callback_data: CountriesTopsCallback
):
    user_with_playlists = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    await cb.message.edit_caption(
        caption = cb.message.caption,
        reply_markup = await kb_choose_pl(
            track_id = callback_data.track_id,
            limit = callback_data.limit,
            offset = callback_data.offset,
            offset_pl = callback_data.offset_pl,
            limit_pl = callback_data.limit_pl,
            country = callback_data.country,
            playlists = user_with_playlists.playlists
        )
    ) 


@country_getting_router.callback_query(CountriesTopsCallback.filter(F.action == "add_pl"))
async def add_track_to_playlist(
    cb: CallbackQuery,
    callback_data: CountriesTopsCallback
):
    await TrackRequestsSQL.add_to_playlist(
        track_id = callback_data.track_id,
        track_name = cb.message.caption,
        playlist_id = callback_data.pl_id
    )

    await cb.answer("Трек добавлен в плейлист")
