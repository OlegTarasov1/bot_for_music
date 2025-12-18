from utils.keyboards.tracks_kb.list_playlists_to_add_track import list_playlists_to_add_track
from utils.keyboards.list_audio_keyboard import list_music_kb
from utils.api_integrations.sound_cloud_api.search import get_soundcloud_track_by_id
from utils.sql_requests.track_requests import TrackRequestsSQL
from schemas.cb_schemas.cb_list_music import MusicCallback
from schemas.cb_schemas.cb_track_callbacks import TrackCallbacks
from schemas.cb_schemas.cb_playlists import PlaylistCallback
from utils.keyboards.playlist_keyboards.retreive_playlist_kb import retreive_playlist
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import get_mp3_links, install_track, delete_file
from utils.keyboards.playlist_keyboards.retreive_audio_from_playlists import retreive_audio_data
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Router, F
import logging
from crude.crude_path import path_vibe_final
import json


track_router = Router()

# хендлер выведения плейлистов, в которые можно добавить трек

@track_router.callback_query(MusicCallback.filter(F.action == "add_pl"))
async def list_tracks_of_playlist(
    cb: CallbackQuery,
    callback_data: MusicCallback
):
    request = cb.message.caption
    
    playlists = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Выберите плейлист:",
        reply_markup = await list_playlists_to_add_track(
            playlists = playlists.playlists,
            track_id = callback_data.track_id,
            request = request
        )
    )

# хендлер для выведения плейлистов пользователя (тоже, что и раньше, по сути)

@track_router.callback_query(TrackCallbacks.filter(F.action == "get"))
async def paginate_through_playlists(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    playlists = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Выберите плейлист:",
        reply_markup = await list_playlists_to_add_track(
            playlists = playlists.playlists,
            track_id = callback_data.track_id,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )

# хендлер для добавления трека в плейлист

@track_router.callback_query(TrackCallbacks.filter(F.action == "add"))
async def add_track_to_playlist(
    cb: CallbackQuery,
    callback_data: TrackCallbacks
):
    track_json = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )

    addition_result = await TrackRequestsSQL.add_to_playlist(
        track_id = callback_data.track_id,
        track_name = track_json.get("title", "No Title"),
        playlist_id = callback_data.playlist_id
    )

    logging.warning('the bug is somewhere here.')
    
    await cb.answer("Трек был добавлен в плейлист")
    # if not addition_result:
    #     await cb.answer("Трек и так уже был в пейлисте")

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Выберите:",
        reply_markup = await list_music_kb(
            request = callback_data.request,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# хендлер для обработки нажатия на трек в плейлисте

@track_router.callback_query(PlaylistCallback.filter(F.action == "audio"))
async def retreive_audio_in_playlist(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    logging.warning(callback_data.track_id)
    logging.warning("worked audio")
    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Выберите:",
        reply_markup = await retreive_audio_data(
            playlist_id = callback_data.playlist_id,
            limit = callback_data.limit,
            offset = callback_data.offset,
            track_offset = callback_data.track_offset,
            track_limit = callback_data.track_limit,
            track_id = callback_data.track_id
        )
    )


# Обработка удаления трека из плейлиста

@track_router.callback_query(PlaylistCallback.filter(F.action == "del_conn"))
async def delete_track_from_playlist(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    await TrackRequestsSQL.delete_track_from_playlist(
        track_id = callback_data.track_id,
        playlist_id = callback_data.playlist_id
    )
    playlist = await TrackRequestsSQL.get_playlist_by_id(
        playlist_id = callback_data.playlist_id
    )

    await cb.answer("Трек был удалён из плейлиста")

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        caption = f"Плейлист: {playlist.title}",
        reply_markup = await retreive_playlist(
            playlist_data = playlist,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Скачивание трека из плейлиста

@track_router.callback_query(PlaylistCallback.filter(F.action == "get_track"))
async def get_track_from_playlist(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    logging.warning(f"track id: {callback_data.track_id}")
    track_data = await get_soundcloud_track_by_id(
        track_id = callback_data.track_id
    )
    
    download_links = await get_mp3_links(track_data)

    if download_links:
        logging.warning("download_links:")
        
        downloaded_filepath = await install_track(
            download_links = download_links
        )

        if downloaded_filepath:
            audio_file = FSInputFile(downloaded_filepath)
            await cb.message.answer_audio(
                audio = audio_file,
                title = track_data.get("title", "no_title")
            )
            await delete_file(filepath = downloaded_filepath)
        else:
            await cb.answer("что-то пошло не так: не удалось скачать файл")
    else:
        await cb.answer("что-то пошло не так: нет ссылок на скачивание")

    