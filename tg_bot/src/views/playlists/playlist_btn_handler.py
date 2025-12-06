from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from utils.sql_requests.track_requests import TrackRequestsSQL
from utils.keyboards.playlist_keyboards.list_playlists_kb import list_playlists_kb
from schemas.cb_schemas.cb_playlists import PlaylistCallback
from schemas.fsm_schemas.playlist_creation import PlaylistCreation
from aiogram.fsm.context import FSMContext
from utils.keyboards.playlist_keyboards.retreive_playlist_kb import retreive_playlist
from crude.crude_path import path_vibe_final
import logging


playlist_router = Router()

# Обработка нажатия кнопки "плейлисты" в меню

@playlist_router.callback_query(F.data == "playlists")
async def list_playlists(
    cb: CallbackQuery
):
    user_data = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    if user_data:
        await cb.message.edit_caption(
            # animation = FSInputFile(path_vibe_final),
            # caption = "Плейлисты:",
            reply_markup = await list_playlists_kb(
                playlists = user_data.playlists
            )
        )    
    else:
        await cb.answer(
            "Что-то пошло не так: вас нет в бд, попробуйте нажать '/start'"
        )


# Cоздание нового плейлиста

@playlist_router.callback_query(F.data == "new_playlist")
async def add_new_platlist(
    cb: CallbackQuery,
    state: FSMContext
):
    await cb.message.delete()
    await state.set_state(PlaylistCreation.title)
    await cb.message.answer("Введите название нового плейлиста.")


@playlist_router.message(PlaylistCreation.title)
async def playlist_creation(
    msg: Message,
    state: FSMContext
):
    await state.clear()

    title = msg.text.strip()
    
    if not title or len(title) > 250:
        await msg.answer("Ввод отменён (некорректное название).")
    else:
        await TrackRequestsSQL.create_playlist(
            new_title = title,
            new_user_id = msg.from_user.id
        )

        await msg.answer(
            text = f"Новый плейлист '{title}' был добавлен."
        )


# получение страниц с плейлистами пользователя

@playlist_router.callback_query(PlaylistCallback.filter(F.action == "get"))
async def get_playlists(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    user_data = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = "Плейлисты:",
        reply_markup = await list_playlists_kb(
            playlists = user_data.playlists,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Обработка получения плейлиста

@playlist_router.callback_query(PlaylistCallback.filter(F.action == "retreive"))
async def retreive_playlists(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    logging.warning(f"Playlist id: {callback_data.playlist_id}")
    playlist = await TrackRequestsSQL.get_playlist_by_id(
        playlist_id = callback_data.playlist_id
    )

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = f"Плейлист: {playlist.title}",
        reply_markup = await retreive_playlist(
            playlist_data = playlist,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )


# Удаление плейлиста

@playlist_router.callback_query(PlaylistCallback.filter(F.action == "delete"))
async def playlist_delete(
    cb: CallbackQuery,
    callback_data: PlaylistCallback
):
    await TrackRequestsSQL.delete_playlist_by_id(
        playlist_id = callback_data.playlist_id,
        user_id = cb.from_user.id
    )

    user_data = await TrackRequestsSQL.get_users_playlists(
        user_id = cb.from_user.id
    )

    await cb.message.edit_caption(
        # animation = FSInputFile(path_vibe_final),
        # caption = f"Плейлисты:",
        reply_markup = await list_playlists_kb(
            playlists = user_data.playlists,
            limit = callback_data.limit,
            offset = callback_data.offset
        )
    )
    
