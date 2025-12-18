from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import Message, ChatMemberUpdated
from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram import Router


delete_user_handler = Router()


@delete_user_handler.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handle_unsubscription(
    evnt: ChatMemberUpdated
):
    await UsersRequestsSQL.activate_deactivate_user_by_id(
        tg_id = evnt.from_user.id,
        toggle_status = False
    )


@delete_user_handler.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_subscription(
    evnt: ChatMemberUpdated
):
    await UsersRequestsSQL.activate_deactivate_user_by_id(
        tg_id = evnt.from_user.id,
        toggle_status = True
    )