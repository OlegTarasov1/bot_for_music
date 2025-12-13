from utils.api_integrations.sound_cloud_api.crude_funcs.get_by_link import async_download_audio_from_video
from utils.api_integrations.auddio_api.get_audio import get_json_by_audio
from utils.api_integrations.sound_cloud_api.crude_funcs.get_direct_links import delete_file
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F

link_router = Router()


# Обработка получения аудио из видео

@link_router.callback_query(F.data == "get_audio")
async def download_audio_from_video(
    cb: CallbackQuery
):
    link = cb.message.text
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


# Обработка выделения аудио из видео

@link_router.callback_query(F.data == "extract_audio")
async def extract_audio_from_video(
    cb: CallbackQuery
):
    link = cb.message.text
    file_link = await async_download_audio_from_video(link)
    await delete_file(
        filepath = file_link
    )
    
    if file_link:
        await get_json_by_audio(
            audio_link = link
        )
    else:
        await cb.answer("Что-то пошло не так")