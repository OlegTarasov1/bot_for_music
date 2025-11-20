from utils.keyboards.tracks_kb.retreival_action import retreival_action_choice
from utils.api_integrations.sound_cloud_api.search import search_for_music
from schemas.cb_schemas.cb_list_music import MusicCallback
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.keyboards.list_audio_keyboard import list_music_kb


retreival_router = Router()


@retreival_router.callback_query(MusicCallback.filter(F.action == "retreive"))
async def handle_track_retreival(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    
    await cb.message.edit_text(
        text = "Выберите:",
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
    await cb.message.edit_text(
        text = "Выберите:",
        reply_markup = await list_music_kb(
            request = callback_data.request,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )