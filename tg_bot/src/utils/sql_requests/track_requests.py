import logging
from models import (
    UsersBase,
    PlaylistsBase,
    SongsBase,
    SongsPlaylistsAssociation
)
from settings.db_settings import async_session
from schemas.pydantic_schemas.users_playlists import UsersPlaylistsSchema
from schemas.pydantic_mixins.playlists_schema import PlaylistMixin
from schemas.pydantic_schemas.playlists_songs import UsersPlaylistsSchema
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
        user = await redis_client_sql.get(f"user_{user_id}")
        if user:
            user_dict = json.loads(user)
            if user_dict.get("playlists"):
                await redis_client_sql.set(
                    f"user_{user_id}",
                    user,
                    ex = 60 * 60 * 24 * 2
                )
            else:
                pass

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

            if user_with_playlists:
                user_to_cache = UsersPlaylistsSchema.model_validate(user_with_playlists)
                await redis_client_sql.set(
                    f"user_{user_with_playlists.id}",
                    user_to_cache.model_dump_json(),
                    ex = 60 * 60 * 24 * 2
                )
                
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
                    
        user_cached = await redis_client_sql.get(f"user_{new_user_id}")
        if user_cached:
            user_cached_dict = json.loads(user_cached)
            if isinstance(user_cached_dict.get("playlists"), list):
                playlist = PlaylistMixin.model_validate(new_playlist)
                user_cached.get("playlists").append(playlist.model_dump_json())
                await redis_client_sql.set(
                    f"user_{new_user_id}",
                    user_cached,
                    ex = 60 * 60 * 24 * 2
                )

        return new_playlist
    
    
    @staticmethod
    async def get_playlist_by_id(
        playlist_id: int
    ) -> PlaylistsBase:
        """получение плейлиста с треками по id плейлиста"""

        playlist = await redis_client_sql.get(f"playlist_{playlist_id}")
        if playlist:
            playlist_dict = json.loads(playlist)
            await redis_client_sql.set(
                f"playlist_{playlist_id}",
                playlist,
                ex = 60 * 60 * 24
            )

            playlist = PlaylistsBase(**playlist_dict)
            return playlist

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

        if playlist_data:
            playlist_to_cache = UsersPlaylistsSchema.model_validate(playlist_data)
            await redis_client_sql.set(
                f"playlist_{playlist_id}",
                playlist_to_cache.model_dump_json(),
                ex = 60 * 60 * 24
            )

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
            
            await redis_client_sql.delete(f"playlist_{playlist_id}")
            await redis_client_sql.delete(f"user_{user_id}")


    @staticmethod
    async def add_to_playlist(
        track_id: int,
        track_name: str,
        playlist_id: int
    ) -> bool:
        """Добавление трека в плейлист и удаление плейлиста из кэша"""

        playlist = await redis_client_sql.get(f"playlist_{playlist_id}")

        async with async_session() as session:
            if playlist:
                playlist_json = json.loads(playlist)
                is_existant = False
                for i in playlist_json.get("songs", []):
                    if i.get("id") == track_id:
                        is_existant = True
            else:
                stmt = (
                    select(
                        SongsPlaylistsAssociation
                    )
                    .where(
                        SongsPlaylistsAssociation.playlist_id == playlist_id,
                        SongsPlaylistsAssociation.song_id == track_id
                    )
                )

                is_existant = await session.execute(stmt)
                is_existant = is_existant.scalar_one_or_none()

            if is_existant:

                return False

            new_song = SongsBase(
                id = track_id,
                song_title = track_name
            )
            session.add(new_song)
            
            await session.flush()

            new_association = SongsPlaylistsAssociation(
                playlist_id = playlist_id,
                song_id = track_id
            )

            session.add(new_association)
            await session.commit()

        await redis_client_sql.delete(f"playlist_{playlist_id}")
            
        return True


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