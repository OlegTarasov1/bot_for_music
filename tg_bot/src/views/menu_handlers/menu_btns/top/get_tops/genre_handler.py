from schemas.cb_schemas.cb_top_genres import GenresTopsCallback
from settings.cache_settings import redis_client
from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.tops.get_genres import get_genres
from utils.keyboards.tops_keybards.kb_genres import get_kb_for_tops_by_genres
import logging
import json


genre_getting_router = Router()


@genre_getting_router.callback_query(GenresTopsCallback.filter(F.action == "get"))
async def country_top_handler(
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
