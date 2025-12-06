from models import UsersBase
from settings.db_settings import async_session
from schemas.pydantic_mixins.user_schema import UserMixin
from sqlalchemy import select
from settings.cache_settings import redis_client_sql
import logging
import json


class UsersRequestsSQL:
    
    @staticmethod
    async def create_new_user(
        chat_id: int,
        tg_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
    ) -> UsersBase:
        async with async_session() as session:
            new_user = UsersBase(
                id = tg_id,
                username = username,
                first_name = first_name,
                last_name = last_name,
                chat_id = chat_id
            )
            session.add(new_user)

            await session.commit()

            # if new_user:
            #     user_to_cache = UserMixin.model_validate(new_user)
            #     await redis_client_sql.set(
            #         f"user_{new_user.id}",
            #         user_to_cache.model_dump_json(),
            #         ex = 60 * 60 *24 * 2
            #     )
            
            return new_user


    @staticmethod
    async def get_user_by_id(
        tg_id: int
    ) -> UsersBase | None:
        
        # cached_user = await redis_client_sql.get(f"user_{tg_id}")
        # if cached_user:
        #     pass_to_user = UserMixin.model_validate_json(cached_user)
        #     user = UsersBase(**pass_to_user.model_dump())
            
        #     await redis_client_sql.set(
        #         f"user_{user.id}",
        #         cached_user,
        #         ex = 60 * 60 * 24 * 2
        #     )
        #     return user

        
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == tg_id
                )
            )

            user = await session.execute(stmt)
            user = user.scalar_one_or_none()

            # if user:
            #     user_to_cache = UserMixin.model_validate(user)
            #     await redis_client_sql.set(
            #         f"user_{user.id}",
            #         user_to_cache.model_dump_json(),
            #         ex = 60 * 60 * 24 * 2
            #     )

            return user