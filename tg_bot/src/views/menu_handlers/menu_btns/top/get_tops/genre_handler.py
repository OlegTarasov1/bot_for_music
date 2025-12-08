from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
from utils.keyboards.tops_keybards.list_playlists_in_tops import list_playlists
from settings.cache_settings import redis_client
from utils.keyboards.tops_keybards.kb_genres_retreival import retreive_genre
from aiogram.types import CallbackQuery, FSInputFile
from utils.keyboards.list_audio_keyboard import list_music_kb
from utils.api_integrations.sound_cloud_api.search import get_soundcloud_track_by_id
from aiogram import Router, F
from aiogram.types import FSInputFile
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import install_track, get_mp3_links, delete_file
from utils.tops.get_genres import get_genres
from utils.keyboards.tops_keybards.kb_genres import get_kb_for_tops_by_genres, kb_track_retreival
from utils.sql_requests.track_requests import TrackRequestsSQL
from settings.cache_settings import redis_client_top
import logging
from crude.crude_path import path_vibe_final
import json


genre_getting_router = Router()


@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "get"))
async def genre_top_list(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    genres = await get_genres()

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Выберите:",
        reply_markup = await get_kb_for_tops_by_genres(
            tags = genres,
            limit = callback_data.limit,
            offset = callback_data.offset 
        )
    )


@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "retreive"))
async def genre_top_retreive(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    logging.warning(callback_data.genre)
    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        reply_markup = await retreive_genre(
            genre = callback_data.genre,
            offset = callback_data.offset       
        )
    )



@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "retreive_track"))
async def track_retreival_handler(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    track_data = await redis_client_top.get(f"track_{callback_data.track_id}")
    if track_data:
        track_data_json = json.loads(track_data)
    else:
        track_data_json = await get_soundcloud_track_by_id(
            track_id=callback_data.track_id
        )
        await redis_client_top.set(
            f"track_{callback_data.track_id}",
            json.dumps(track_data_json),
            ex = 60 * 60 * 24 * 2
        )
    
    await cb.message.edit_caption(
        caption = track_data_json.get("title", ''),
        animation = FSInputFile(path_vibe_final),
        reply_markup = await kb_track_retreival(
            limit = callback_data.limit,
            offset = callback_data.offset,
            track_id = callback_data.track_id,
            genre = callback_data.genre
        )
    )


# Добавление трека из топов в избранное 

@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "add_fav"))
async def add_track_from_top_to_favorits(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    
    track_id = callback_data.track_id    
    
    track_data = await redis_client_top.get(f"track_{track_id}")

    if track_data:
        track_data = json.loads(track_data)
        if int(track_data.get("id")) == track_id:
            track_name = str(track_data.get("title", "None"))
    else:
        track_data = await get_soundcloud_track_by_id(
            track_id=track_id
        )
        logging.warning(track_data)
        track_name = track_data.get("title", "None")
        await redis_client_top.set(
            f"track_{track_id}",
            json.dumps(track_data),
            ex = 60 * 60 * 24 * 2
        )

    await TrackRequestsSQL.add_track_to_favorits(
        track_id = callback_data.track_id,
        user_id = cb.from_user.id,
        track_name = track_name 
    )

    await cb.answer("Трек добавлен в избранное.")



# Обработка добавления в плейлисты (выведение списка плейлистов)

@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "list_pl"))
async def list_playlists_to_add_track_to(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    user_data = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )
    logging.warning(callback_data.genre)
    await cb.message.edit_caption(
        caption = cb.message.caption,
        reply_markup = await list_playlists(
            playlists=user_data.playlists,
            limit=callback_data.limit,
            offset=callback_data.offset,
            offset_pl=callback_data.offset_pl,
            limit_pl=callback_data.limit_pl,
            genre = callback_data.genre,
            track_id = callback_data.track_id
        )
    )


# add_pl Обработка добавления трека в плейлист

@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "add_pl"))
async def additioning_track_to_playlist(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    track_name = cb.message.caption
    await TrackRequestsSQL.add_to_playlist(
        track_id = callback_data.track_id,
        track_name = track_name,
        playlist_id = callback_data.playlist_id
    )

    await cb.answer("Трек добавлен в плейлист.")