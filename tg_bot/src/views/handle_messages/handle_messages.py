from utils.api_integrations.sound_cloud_api.search import search_for_music
from utils.keyboards.list_audio_keyboard import list_music_kb
from settings.cache_settings import redis_client
from aiogram.types import Message
from aiogram import Router, F
import logging
import json


messages_router = Router()


@messages_router.message(F.text)
async def handle_text(msg: Message):
    request = msg.text.strip().lower()
    
    await msg.answer(
        text = "выберите:",
        reply_markup = await list_music_kb(
            request = request
        )
    )





@messages_router.message(F.audio)
async def handle_audio(msg: Message):
    await msg.answer("not yet finished")


@messages_router.message(F.video)
async def handle_video(msg: Message):
    await msg.answer("not yet finished")