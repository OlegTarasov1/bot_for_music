from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
from settings.cache_settings import redis_client
from utils.keyboards.tops_keybards.kb_genres_retreival import retreive_genre
from aiogram.types import CallbackQuery
from utils.keyboards.list_audio_keyboard import list_music_kb
from utils.api_integrations.sound_cloud_api.search import get_soundcloud_track_by_id
from aiogram import Router, F
from aiogram.types import FSInputFile
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import install_track, get_mp3_links, delete_file
from utils.tops.get_genres import get_genres
from utils.keyboards.tops_keybards.kb_genres import get_kb_for_tops_by_genres, kb_track_retreival
import logging
import json


genre_getting_router = Router()


@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "get"))
async def genre_top_list(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    genres = await get_genres()

    await cb.message.edit_text(
        text = "Выберите:",
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
    await cb.message.edit_text(
        text = "Выбрите:",
        reply_markup = await retreive_genre(
            genre = callback_data.genre.replace(" ", "_"),
            offset = callback_data.offset       
        )
    )



@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "retreive_track"))
async def track_retreival_handler(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    await cb.message.edit_text(
        text = "Выберите:",
        reply_markup = await kb_track_retreival(
            limit = callback_data.limit,
            offset = callback_data.offset,
            track_id = callback_data.track_id
        )
    )


@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "download"))
async def download_track(
    cb: CallbackQuery,
    callback_data: GenresTopsCallback
):
    logging.warning(f"getting track by id...:{callback_data.track_id}")
    track_json = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )

    track_links = await get_mp3_links(track_json)
    file_dir = await install_track(track_links)

    audio_file = FSInputFile(
        path = file_dir
    )

    await cb.message.answer_audio(
        audio = audio_file,
        title = "test"
    )

    await delete_file(file_dir)