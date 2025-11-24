from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.keyboards.tops_get import tops_kb
from utils.keyboards.tops_keybards.kb_countries import get_kb_for_tops_by_countries
from utils.tops.get_genres import get_genres
from utils.keyboards.tops_keybards.kb_genres import get_kb_for_tops_by_genres
from .get_tops.country_handler import country_getting_router
from .get_tops.genre_handler import genre_getting_router

tops_router = Router()

tops_router.include_router(country_getting_router)
tops_router.include_router(genre_getting_router)


@tops_router.callback_query(F.data == "tops")
async def get_tops(cb: CallbackQuery):
    await cb.message.edit_text(
        text = "Как ранжировать топы:",
        reply_markup = tops_kb
    )


@tops_router.callback_query(F.data == "tops_by_genres")
async def get_tops_by_genres(cb: CallbackQuery):

    tags = await get_genres()

    keyboard = await get_kb_for_tops_by_genres(
        tags = tags
    )

    await cb.message.edit_text(
        text = "выберите жанр:",
        reply_markup = keyboard
    )


@tops_router.callback_query(F.data == "tops_by_countries")
async def get_tops_by_countries(cb: CallbackQuery):
    
    keyboard = await get_kb_for_tops_by_countries()

    await cb.message.edit_text(
        text = "выберите страну:",
        reply_markup = keyboard
    )