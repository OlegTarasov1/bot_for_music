from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import ErrorEvent
import logging
from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import IS_MEMBER, IS_NOT_MEMBER


delete_user_handler = Router()


# Обработка блокировки бота

@delete_user_handler.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(IS_MEMBER >> IS_NOT_MEMBER))
)
async def handle_unsubscription(event: ChatMemberUpdated):
    user_id = event.from_user.id
    await UsersRequestsSQL.activate_deactivate_user_by_id(
        user_id,
        False
    )
    


# Обработка разблокировки бота

@delete_user_handler.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(IS_NOT_MEMBER >> IS_MEMBER))
)
async def on_unblock_without_message(event: ChatMemberUpdated):
    user_id = event.from_user.id
    await UsersRequestsSQL.activate_deactivate_user_by_id(
        user_id,
        True
    )
    




