from aiogram.types import Message
from aiogram import Router, F

messages_router = Router()


@messages_router.message(F.text)
async def handle_text(msg: Message):
    await msg.answer("not yet finished")


@messages_router.message(F.audio)
async def handle_audio(msg: Message):
    await msg.answer("not yet finished")


@messages_router.message(F.video)
async def handle_video(msg: Message):
    await msg.answer("not yet finished")