from utils.api_integrations.sound_cloud_api.crude_funcs.get_by_link import async_download_audio_from_video
from utils.api_integrations.auddio_api.get_audio import get_json_by_audio
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import delete_file
from aiogram.types import Message, CallbackQuery, FSInputFile
from crude.crude_path import path_vibe_final
from utils.keyboards.list_audio_keyboard import list_music_kb
from aiogram import Router, F
import logging


link_router = Router()


# Обработка получения аудио из видео

@link_router.callback_query(F.data == "get_audio")
async def download_audio_from_video(
    cb: CallbackQuery
):
    link = cb.message.text
    await cb.message.delete()
    pending_message = await cb.message.answer(
        text = "скачивание трека..."
    )
    try:
        file_link = await async_download_audio_from_video(link)
        if file_link:
            audio_file = FSInputFile(file_link)
            await cb.message.answer_audio(
                audio = audio_file,
                title = "audio_from_video"
            )
            await delete_file(
                filepath = file_link
            )
        else:
            await cb.answer("Что-то пошло не так, не вышло скачать.")
    except Exception as e:
        await cb.message.answer("что-то пошло не так, вероятно трека не было")
        logging.error(e)
    finally:
        await pending_message.delete()


# Обработка выделения аудио из видео

@link_router.callback_query(F.data == "extract_audio")
async def extract_audio_from_video(
    cb: CallbackQuery
):
    link = cb.message.text
    await cb.message.delete()
    pending_message = await cb.message.answer("скачивание...")

    file_link = await async_download_audio_from_video(link)


    try:
        if file_link:
            await pending_message.edit_text(
                text = "поиск трека..."
            )
            audio_data = await get_json_by_audio(
                audio_link = file_link
            )
            if audio_data.get("result", dict()).get("title"):
                request = f"{audio_data.get('result', dict()).get('title', '')}, {audio_data.get('result', dict()).get('artist', '')}"
                await cb.message.answer_animation(
                    caption = request,
                    animation = FSInputFile(path_vibe_final),
                    reply_markup = await list_music_kb(
                        request = request
                    )
                )
            else:
                await cb.message.answer("Не было найдено трека, к сожалению")
        else:
            await cb.answer("Что-то пошло не так, вероятно трек не был найден")

    except Exception as e:
        logging.warning(e)
        await cb.message.answer(
            "что-то пошло не так"
        )

    finally:
        await pending_message.delete()
        await delete_file(
            filepath = file_link
        )