from utils.sql_requests.track_requests import TrackRequestsSQL
from utils.keyboards.menus.list_favorit_tracks import list_favorit_tracks_kb
from aiogram.types import CallbackQuery
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from utils.api_integrations.sound_cloud_api.search import get_soundcloud_track_by_id
from settings.cache_settings import redis_client
from utils.keyboards.favorits.retreive_favorit_track_kb import retreive_favorit_track_kb
from aiogram import Router, F
import logging
import json


favorit_router = Router()


# Получение списка избранных треков

@favorit_router.callback_query(TrackCallbacks.filter(F.action == "get_fav"))
async def list_favorits(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    user_with_favorit_tracks = await TrackRequestsSQL.get_favorit_tracks(
        user_id = cb.from_user.id
    ) 

    await cb.message.edit_caption(
        reply_markup = await list_favorit_tracks_kb(
            tracks_list = user_with_favorit_tracks.favorite_tracks,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Обработка добавления трека в список избранных

@favorit_router.callback_query(TrackCallbacks.filter(F.action == "add_fav"))
async def add_track_to_favorit(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    
    track_id = callback_data.track_id    
    
    track_data = await redis_client.get(cb.message.caption)

    if track_data:
        track_data = json.loads(track_data)
        for i in track_data:
            if int(i.get("id")) == track_id:
                track_name = str(i.get("title", "None"))
                break
    else:
        track_data = await get_soundcloud_track_by_id(
            track_id=track_id
        )
        logging.warning(track_data)
        track_name = track_data.get("title", "None")

    await TrackRequestsSQL.add_track_to_favorits(
        track_id = callback_data.track_id,
        user_id = cb.from_user.id,
        track_name = track_name 
    )

    await cb.answer("Трек добавлен в избранное.")


# Обработка получения трека из списка избранных

@favorit_router.callback_query(TrackCallbacks.filter(F.action == "retreive_fav"))
async def retreive_track_from_favorits(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    await cb.message.edit_caption(
        reply_markup = await retreive_favorit_track_kb(
            track_id = callback_data.track_id,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Обработка удаления трека из списка избранных

@favorit_router.callback_query(TrackCallbacks.filter(F.action == "del_fav"))
async def delete_from_favorit(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    await TrackRequestsSQL.delete_track_from_favorits(
        track_id = callback_data.track_id,
        user_id = cb.from_user.id
    )

    user_with_favorit_tracks = await TrackRequestsSQL.get_favorit_tracks(
        user_id = cb.from_user.id
    ) 

    await cb.message.edit_caption(
        reply_markup = await list_favorit_tracks_kb(
            tracks_list = user_with_favorit_tracks.favorite_tracks,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )

    await cb.answer("Трек удалён из избранных")