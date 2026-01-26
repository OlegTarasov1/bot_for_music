from pydub import AudioSegment
from uuid import uuid4
import asyncio
import os
from ffmpeg.asyncio import FFmpeg
from pathlib import Path


# Функция для конвертацтт ogg в mp3 (голосовое в mp3)

async def convert_ogg_to_mp3(
    file_path: Path
) -> Path:
    if file_path.suffix.lower() == ".ogg":
        audio = await asyncio.to_thread(
            AudioSegment.from_ogg,
            file_path
        )
        new_file_path = file_path.with_suffix(".mp3")
        await asyncio.to_thread(
            audio.export,
            new_file_path,
            format = "mp3",
            bitrate = "128k"
        )
        
    return new_file_path



# функция для выделения из видео аудио

async def convert_video_to_mp3(
    file_path: Path
) -> Path:
    new_path = file_path.with_suffix('.mp3')

    ffmpeg = (
        FFmpeg()
        .input(str(file_path))
        .output(
            str(new_path),
            {"vn": None},          # Убираем видео
            acodec='libmp3lame',   # Кодируем в mp3
            ab='192k'              # Битрейт (опционально)
        )
    )

    await ffmpeg.execute()
    return new_path