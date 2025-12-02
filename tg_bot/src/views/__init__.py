from .handle_messages.handle_messages import messages_router
from .menu_handlers.start_handler import menu_router
from .other_handlers.menu_handler.get_menu_handler import get_menu_router
from .other_handlers.shutter_handler.shutter_router import shutter_router
from .playlists.playlist_btn_handler import playlist_router
from .track_handlers.track_handlers import track_router
from aiogram import Router

master_router = Router()

master_router.include_router(shutter_router)
master_router.include_router(get_menu_router)
master_router.include_router(menu_router)
master_router.include_router(playlist_router)
master_router.include_router(track_router)

master_router.include_router(messages_router)