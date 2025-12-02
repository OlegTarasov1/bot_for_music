from utils.keyboards.tracks_kb.retreival_action import retreival_action_choice
from utils.api_integrations.sound_cloud_api.search import search_for_music, get_soundcloud_track_by_id
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
from utils.keyboards.list_audio_keyboard import list_music_kb
import logging
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import get_mp3_links, install_track, delete_file

retreival_router = Router()


@retreival_router.callback_query(MusicCallback.filter(F.action == "retreive"))
async def handle_track_retreival(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    
    await cb.message.edit_caption(
        caption = "Выберите:",
        reply_markup = await retreival_action_choice(
            track_id = callback_data.track_id,
            offset = callback_data.offset,
            limit = callback_data.limit,
            request = callback_data.request            
        )
    )


@retreival_router.callback_query(MusicCallback.filter(F.action == "get"))
async def handle_track_retreival(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    await cb.message.edit_caption(
        caption = "Выберите:",
        reply_markup = await list_music_kb(
            request = callback_data.request,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )

@retreival_router.callback_query(MusicCallback.filter(F.action == "download"))
async def download_handler(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    await cb.message.edit_caption(
        # caption = "Выберите:",
        reply_markup = await list_music_kb(
            request = callback_data.request,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )
    
    track_data = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )
    
    download_links = await get_mp3_links(track_data)

    if download_links:
        logging.warning("download_links:")
        
        downloaded_filepath = await install_track(
            download_links = download_links
        )

        if downloaded_filepath:
            audio_file = FSInputFile(downloaded_filepath)
            await cb.message.answer_audio(
                audio = audio_file,
                title = track_data.get("title", "no_title")
            )
            await delete_file(filepath = downloaded_filepath)
        else:
            await cb.answer("что-то пошло не так: не удалось скачать файл")
    else:
        await cb.answer("что-то пошло не так: нет ссылок на скачивание")

    