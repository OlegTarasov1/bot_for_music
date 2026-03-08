from utils.keyboards.tracks_kb.retreival_action import retreival_action_choice
from utils.api_integrations.sound_cloud_api.search import search_for_music, get_soundcloud_track_by_id
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.types import CallbackQuery, URLInputFile, FSInputFile
from aiogram import Router, F
from utils.keyboards.list_audio_keyboard import list_music_kb
from aiogram.enums import ParseMode
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import get_mp3_links, install_track, delete_file, get_direct_mp3_links
from utils.extra_funcs.cache_name import retreive_name_from_cache, set_name_in_cache
from utils.extra_funcs.get_ad import show_advert
import logging
import os


retreival_router = Router()


@retreival_router.callback_query(MusicCallback.filter(F.action == "retreive"))
async def handle_track_retreival(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    # request = cb.message.caption
    request = await retreive_name_from_cache(
        user_id = cb.from_user.id,
        msg_id = cb.message.message_id
    )
    logging.warning(f"{cb.from_user.id}:{cb.message.message_id}: {request}")
    track_data = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )

    await cb.message.edit_caption(
        caption = " - ".join(
            filter(
                None,
                [
                    track_data.get("artist", None),
                    track_data.get("title", "")
                ]
            )
        ),
        reply_markup = await retreival_action_choice(
            track_id = callback_data.track_id,
            offset = callback_data.offset,
            limit = callback_data.limit,
            request = request            
        )
    )


@retreival_router.callback_query(MusicCallback.filter(F.action == "get"))
async def handle_track_retreival(
    cb: CallbackQuery,
    callback_data: MusicCallback
):


    request = await retreive_name_from_cache(
        user_id = cb.from_user.id,
        msg_id = cb.message.message_id
    )
    
    logging.warning(f"{cb.from_user.id}:{cb.message.message_id}: {request}")

    logging.warning(f"request: {request}")

    await cb.message.edit_caption(
        # caption = request,
        reply_markup = await list_music_kb(
            request = request,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# track download handler

@retreival_router.callback_query(MusicCallback.filter(F.action == "download"))
async def download_handler(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    notice_message = await cb.message.answer(
        "Загрузка... ⌛"
    )
    track_data = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )
    logging.warning(f"track_data: {track_data}")

    download_links = await get_direct_mp3_links(track_data)

    if download_links:
        logging.warning(f"direct download link: {download_links[0]}")
        await cb.message.answer_audio(
            audio = URLInputFile(download_links[0]),
            title = track_data.get("title", "no title"),
            performer = track_data.get("uploader", "no artist"),
            parse_mode = ParseMode.HTML,
            caption = f"<a href = '{os.getenv('BOT_LINK')}'>🔊 Нажми, чтобы найти песню</a>"
        )

    else:
        download_links = await get_mp3_links(track_data)

        if download_links:
            logging.warning(f"\n\ndownload_links: {download_links}")
            
            downloaded_filepath = await install_track(
                download_links = download_links
            )

            if downloaded_filepath:
                audio_file = FSInputFile(downloaded_filepath)
                await cb.message.answer_audio(
                    audio = audio_file,
                    title = track_data.get("title", "no title"),
                    performer = track_data.get("uploader", "no artist"),
                    parse_mode = ParseMode.HTML,
                    caption = f"<a href = '{os.getenv('BOT_LINK')}'>🔊 Нажми, чтобы найти песню</a>"        
                )
                await delete_file(filepath = downloaded_filepath)
            else:
                await cb.answer("что-то пошло не так: не удалось скачать файл")
        else:
            await cb.answer("что-то пошло не так: нет ссылок на скачивание")

    await notice_message.delete()
    await show_advert(cb.from_user.id)
    