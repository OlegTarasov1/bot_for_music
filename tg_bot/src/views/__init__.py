from aiogram import Router
from .user_data.user_api import user_router


master_router = Router()

master_router.include_router(user_router)