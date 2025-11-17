from aiogram import Router, F
from aiogram.types import CallbackQuery


shutter_router = Router()

@shutter_router.callback_query(F.data == "shutter")
async def get_shutter(cb: CallbackQuery):
    await cb.answer(
        text = "Ручка пока не закончена." 
    )