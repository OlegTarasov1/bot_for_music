from models import UsersBase
from datetime import datetime
from settings.db_settings import async_session
from schemas.pydantic_mixins.user_schema import UserMixin
from sqlalchemy import select, delete, update
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

            await session.refresh(new_user)

            user_json = UserMixin.model_validate(new_user)

            await redis_client_sql.set(
                f"user_{new_user.id}",
                user_json.model_dump_json(),
                ex = 60 * 60 * 24 * 2
            ) 

            return new_user
            

    @staticmethod
    async def get_user_by_id(
        tg_id: int
    ) -> UsersBase | None:

        cached_data = await redis_client_sql.get(
            f"user_{tg_id}"
        )
        if cached_data:
            user_data = UserMixin.model_validate_json(cached_data)
            user = UsersBase(**user_data.model_dump())

            return user

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

            if user:
                user_to_cache = UserMixin.model_validate(user)

                await redis_client_sql.set(
                    f"user_{user.id}",
                    user_to_cache.model_dump_json(),
                    ex = 60 * 60 * 24 * 2
                )

            return user

        

    @staticmethod
    async def get_all_users() -> list[UsersBase]:
        """Возвращает список пользователей (не админов)"""
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.is_admin == False
                )
            )
            
            users_list = await session.execute(stmt)
            users_list = users_list.scalars().all()

            return users_list
        

    @staticmethod
    async def activate_deactivate_user_by_id(
        tg_id: int,
        toggle_status: bool
    ) -> None:
        """Обработка удаления пользователя по id из бд и из кэша"""
        await redis_client_sql.delete(
            f"user_{tg_id}"
        )

        async with async_session() as session:
            stmt = (
                update(
                    UsersBase
                )
                .values(
                    UsersBase.is_active == toggle_status,
                    UsersBase.activation_toggle_time == datetime.now()
                )
                .where(
                    UsersBase.id == tg_id
                )
            )
            
            await session.execute(stmt)
            await session.commit()


        