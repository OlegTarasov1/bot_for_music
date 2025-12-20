from aiogram.filters import ChatMemberUpdatedFilter, LEFT, KICKED
from aiogram.types import Message, ChatMemberUpdated
from utils.sql_requests.user_requests import UsersRequestsSQL
from aiogram import Router


delete_user_handler = Router()


@delete_user_handler.chat_member(ChatMemberUpdatedFilter(member_status_changed = LEFT | KICKED))
async def handle_unsubscription(
    evnt: ChatMemberUpdated
):
    await UsersRequestsSQL.activate_deactivate_user_by_id(
        tg_id = evnt.from_user.id,
        toggle_status = False
    )


# @delete_user_handler.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOINED))
# async def handle_subscription(
#     evnt: ChatMemberUpdated
# ):
#     await UsersRequestsSQL.activate_deactivate_user_by_id(
#         tg_id = evnt.from_user.id,
#         toggle_status = True
#     )