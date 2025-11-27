from models import UsersBase, PlaylistsBase
from settings.db_settings import async_session
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload


class TrackRequestsSQL:
    
    @staticmethod
    async def get_users_playlists(
        user_id: int
    ) -> UsersBase | None:
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == user_id
                )
                .options(
                    joinedload(
                        UsersBase.playlists
                    )
                )
            )

            data = await session.execute(stmt)
            user_with_playlists = data.unique().scalar_one_or_none()

            return user_with_playlists


    @staticmethod
    async def create_playlist(
        new_title: str,
        new_user_id: int
    ):
        async with async_session() as session:
            new_playlist = PlaylistsBase(
                user_id = new_user_id,
                title = new_title
            )
            
            session.add(new_playlist)
            await session.commit()

        return new_playlist
    
    
    @staticmethod
    async def get_playlist_by_id(
        playlist_id: int
    ) -> PlaylistsBase:
        async with async_session() as session:
            stmt = (
                select(
                    PlaylistsBase
                )
                .where(
                    PlaylistsBase.id == playlist_id
                )
                .options(
                    selectinload(
                        PlaylistsBase.songs
                    )
                )
            )

            playlist_data = await session.execute(stmt)
            playlist_data = playlist_data.unique().scalar_one_or_none()

        return playlist_data
            

    @staticmethod
    async def delete_playlist_by_id(
        playlist_id: int
    ) -> None:
        async with async_session() as session:
            stmt = (
                delete(
                    PlaylistsBase
                )
                .where(
                    PlaylistsBase.id == playlist_id
                )
            )

            await session.execute(stmt)
            await session.commit()

