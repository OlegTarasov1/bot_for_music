from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.raw_texts.texts import search_text

search_btn_router = Router()


@search_btn_router.callback_query(F.data == "handle_search")
async def handle_search(cb: CallbackQuery):
    await cb.message.answer(
        text = search_text
    )