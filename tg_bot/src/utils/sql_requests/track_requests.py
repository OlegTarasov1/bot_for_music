import logging
from datetime import datetime
from models import (
    UsersBase,
    PlaylistsBase,
    SongsBase,
    SongsPlaylistsAssociation,
    FavoritTracksAssociation
)
from sqlalchemy.dialects.postgresql import insert as insert_psql
from settings.db_settings import async_session
from schemas.pydantic_schemas.users_playlists import UsersPlaylistsSchema
from schemas.pydantic_mixins.playlists_schema import PlaylistMixin
from schemas.pydantic_mixins.user_schema import UserMixin
from schemas.pydantic_schemas.playlists_songs import PlaylistsSongsSchema
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload
from settings.cache_settings import redis_client_sql
import json



class TrackRequestsSQL:
    
    @staticmethod
    async def get_users_playlists(
        user_id: int
    ) -> UsersBase | None:
        '''получение пользователя и его плейлистов + кэширование на 2 дня'''
        # user = await redis_client_sql.get(f"user_{user_id}")
        # if user:
        #     user_dict = json.loads(user)
        #     if type(user_dict.get("playlists")) == list:
        #         user_to_model = UsersPlaylistsSchema.model_validate(user_dict)
        #         user_dict = user_to_model.model_dump()
        #         playlists = user_dict.pop("playlists")
        #         user_to_return = UsersBase(**user_dict)
        #         user_to_return.playlists = [
        #             PlaylistsBase(**i)
        #             for i in playlists
        #         ]

        #         return user_to_return

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

            # if user_with_playlists:
            #     user_to_cache = UsersPlaylistsSchema.model_validate(user_with_playlists)
            #     logging.warning(f"user with playlists data: {user_to_cache.model_dump_json()}")
            #     await redis_client_sql.set(
            #         f"user_{user_with_playlists.id}",
            #         user_to_cache.model_dump_json(),
            #         ex = 60 * 60 * 24 * 2
            #     )
                
            return user_with_playlists


    @staticmethod
    async def create_playlist(
        new_title: str,
        new_user_id: int
    ) -> PlaylistsBase:
        '''создание плейлиста пользователя'''

        async with async_session() as session:
            new_playlist = PlaylistsBase(
                user_id = new_user_id,
                title = new_title
            )
            
            session.add(new_playlist)
            await session.commit()
                
        # await redis_client_sql.delete(f"user_{new_user_id}")

        return new_playlist
    
    
    @staticmethod
    async def get_playlist_by_id(
        playlist_id: int
    ) -> PlaylistsBase:
        """получение плейлиста с треками по id плейлиста"""

        # playlist = await redis_client_sql.get(f"playlist_{playlist_id}")
        # if playlist:
        #     playlist_dict = json.loads(playlist)
        #     await redis_client_sql.set(
        #         f"playlist_{playlist_id}",
        #         playlist,
        #         ex = 60 * 60 * 24
        #     )

        #     playlist = PlaylistsBase(**playlist_dict)
        #     return playlist

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

        # if playlist_data:
        #     playlist_to_cache = PlaylistsSongsSchema.model_validate(playlist_data)
        #     await redis_client_sql.set(
        #         f"playlist_{playlist_id}",
        #         playlist_to_cache.model_dump_json(),
        #         ex = 60 * 60 * 24
        #     )

        return playlist_data
            

    @staticmethod
    async def delete_playlist_by_id(
        user_id: int,
        playlist_id: int
    ) -> None:
        """Удаление плейлиста + удаление плейлиста и пользователя, связанного с плейлистом из кэша"""
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
            
            # await redis_client_sql.delete(f"playlist_{playlist_id}")
            # await redis_client_sql.delete(f"user_{user_id}")


    @staticmethod
    async def add_to_playlist(
        track_id: int,
        track_name: str,
        playlist_id: int
    ) -> None:
        """Добавление трека в плейлист и удаление плейлиста из кэша"""

        async with async_session() as session:

            stmt = (
                select(
                    SongsBase
                )
                .where(
                    SongsBase.id == track_id
                )
            )

            is_existant = await session.execute(stmt)
            is_existant = is_existant.scalar_one_or_none()

            if not is_existant:
                
                new_song = SongsBase(
                    id = track_id,
                    song_title = track_name
                )
                session.add(new_song)
                await session.flush()
                
            stmt = (
                insert_psql(
                    SongsPlaylistsAssociation
                )
                .values(
                    playlist_id = playlist_id,
                    song_id = track_id
                )
                .on_conflict_do_update(
                    index_elements = ["song_id", "playlist_id"],
                    set_={
                        "time_added": datetime.now()
                    }
                )
            )
            await session.execute(stmt)
            await session.commit()


    @staticmethod
    async def delete_track_from_playlist(
        track_id: int,
        playlist_id: int
    ) -> None:
        """Удаление трека и удаление плейлиста из кэша"""

        async with async_session() as session:
            stmt = (
                delete(
                    SongsPlaylistsAssociation
                )
                .where(
                    SongsPlaylistsAssociation.song_id == track_id,
                    SongsPlaylistsAssociation.playlist_id == playlist_id
                )
            )

            await session.execute(stmt)
            await session.commit()

        await redis_client_sql.delete(f"playlist_{playlist_id}")


    @staticmethod
    async def get_favorit_tracks(
        user_id: int
    ) -> UsersBase:
        """Функция возвращает пользователя с треками из списка favorit"""
        async with async_session() as session:
            stmt = (
                select(
                    UsersBase
                )
                .where(
                    UsersBase.id == user_id
                )
                .options(
                    selectinload(
                        UsersBase.favorite_tracks
                    )
                )
            )

            user_data = await session.execute(stmt)
            user_with_tracks = user_data.scalar_one_or_none()

        return user_with_tracks


    @staticmethod
    async def add_track_to_favorits(
        track_id: int,
        user_id: int,
        track_name: str
    ) -> bool:
        """Добавление трека в список Favorit пользователя"""
        async with async_session() as session:
            
            stmt = (
                select(
                    SongsBase
                )
                .where(
                    SongsBase.id == track_id
                )
            )

            is_existant = await session.execute(stmt)
            
            is_existant = is_existant.scalar_one_or_none()

            if not is_existant:
                new_track = SongsBase(
                    id = track_id,
                    song_title = track_name
                )
                session.add(new_track)
                await session.flush()


            stmt = (
                insert_psql(
                    FavoritTracksAssociation
                )
                .values(
                    user_id = user_id,
                    song_id = track_id
                )
                .on_conflict_do_update(
                    index_elements = ["user_id", "song_id"],
                    set_={
                        "time_added": datetime.now()
                    }
                )
            )

            await session.execute(stmt)

            await session.commit()


    @staticmethod
    async def delete_track_from_favorits(
        track_id: int,
        user_id: int    
    ) -> None:
        """Удаление связи между треком и пользователем (FavoritTracksAssociation)"""
        async with async_session() as session:
            stmt = (
                delete(
                    FavoritTracksAssociation
                )
                .where(
                    FavoritTracksAssociation.song_id == track_id,
                    FavoritTracksAssociation.user_id == user_id
                )
            )

            await session.execute(stmt)
            await session.commit()