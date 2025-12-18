from utils.api_integrations.sound_cloud_api.search import search_for_music
from utils.api_integrations.auddio_api.get_audio import get_json_by_audio
from utils.keyboards.list_audio_keyboard import list_music_kb
from .msg_callbacks.retreive_track import retreival_router
from utils.keyboards.link_processing_kbs.link_received_kb import link_received_kb 
from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import delete_file
from crude.crude_path import path_vibe_final
from views.handle_messages.msg_callbacks.link_handlers import link_router
from utils.extra_funcs.ogg_to_mp3 import convert_ogg_to_mp3
from uuid import uuid4
from pathlib import Path
import logging
import json



messages_router = Router()

messages_router.include_router(retreival_router)
messages_router.include_router(link_router)


@messages_router.message(F.text)
async def handle_text(msg: Message):

    request = msg.text.strip()

    if request.startswith('http'):
        await msg.delete()

        await msg.answer(
            text = request,
            reply_markup = await link_received_kb()
        )
    else:
        await msg.answer_animation(
            caption = request,
            animation = FSInputFile(path_vibe_final),
            reply_markup = await list_music_kb(
                request = request 
            )
        )


# Получает аудио, конвертирует в mp3
# Получает данные о треке с аудио через сторонний сервис
@messages_router.message(F.audio | F.voice)
async def handle_audio(msg: Message):
    folder_path = Path(__file__).parent.parent.parent / "media"

    pending_message = await msg.answer(
        text = "скачивается"
    )
    if msg.audio:
        file_path = folder_path / f"{uuid4()}.mp3"
        audio_id = msg.audio.file_id

    elif msg.voice:
        file_path = folder_path / f"{uuid4()}.ogg"
        audio_id = msg.voice.file_id
    
    audio_path = await msg.bot.get_file(audio_id)
    await audio_path.bot.download_file(
        file_path = audio_path.file_path,
        destination = file_path
    )
    if str(file_path).split(".")[-1] == "ogg":
        new_path = await convert_ogg_to_mp3(
            file_path = file_path
        )
        await delete_file(
            filepath = str(file_path)
        )

        file_path = new_path

    try:
        await pending_message.edit_text(
            text = "поиск подходящего трека..."
        )
        request = await get_json_by_audio(file_path)
        if request.get("result", dict()).get("title", None):
            await msg.answer(
                text = request.get("result", dict()).get("title", None)
            )
            await msg.answer(
                reply_markup = await list_music_kb(
                    request = request.get("result", dict()).get("title")
                )
            )

    except Exception as e:
        logging.error(e)
        await msg.answer("что-то пошло не так")

    finally:
        await pending_message.delete()
        
        await delete_file(
            filepath = str(file_path)
        )



@messages_router.message(F.video)
async def handle_video(msg: Message):
    await msg.answer("not yet finished")