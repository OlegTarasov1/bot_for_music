from aiogram.types import CallbackQuery
from aiogram import Router, F
from utils.keyboards.tops_get import tops_kb

tops_router = Router()


@tops_router.callback_query(F.data == "tops")
async def get_tops(cb: CallbackQuery):
    await cb.message.edit_text(
        text = "Как ранжировать топы:",
        reply_markup = tops_kb
    )
