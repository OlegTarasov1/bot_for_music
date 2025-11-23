from utils.api_integrations.sound_cloud_api.search import search_for_music
from utils.api_integrations.auddio_api.get_audio import get_json_by_audio
from utils.keyboards.list_audio_keyboard import list_music_kb
from settings.cache_settings import redis_client
from .msg_callbacks.retreive_track import retreival_router
from aiogram.types import Message
from aiogram import Router, F
import logging
import json


messages_router = Router()

messages_router.include_router(retreival_router)


@messages_router.message(F.text)
async def handle_text(msg: Message):
    request = msg.text.strip().lower()
    
    await msg.answer(
        text = "выберите:",
        reply_markup = await list_music_kb(
            request = request
        )
    )


@messages_router.message(F.audio | F.voice)
async def handle_audio(msg: Message):
    # msg.audio.file_id
    audio = msg.audio if msg.audio else msg.voice
    print(audio)
    request = await get_json_by_audio(audio)
    if request.get("result", dict()).get("title", None):
        print(request.get("result", dict())["title"])
        await msg.answer(
            text = "выберите:",
            reply_markup = await list_music_kb(
                request = "eminem"
            )
        )


@messages_router.message(F.video)
async def handle_video(msg: Message):
    await msg.answer("not yet finished")