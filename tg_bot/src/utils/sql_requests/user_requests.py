from models import UsersBase
from settings.db_settings import async_session
from sqlalchemy import select


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

            return new_user


    @staticmethod
    async def get_user_by_id(
        tg_id: int
    ) -> UsersBase | None:
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

            return user