from pathlib import Path
from uuid import uuid4
import logging
import asyncio
import yt_dlp
import os


async def async_download_audio_from_video(
    url: str
) -> str | None:
    """
    Скачивает лучшее доступное аудио по ссылке Работает с YouTube, TikTok, Instagram, Twitter/X, Vimeo и т.д.
    """
    output_link = Path("/app/media")
    file_name = uuid4()
    output_template = str(output_link / f"{file_name}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'playlist_items': '1',
        'quiet': True,
        'no_warnings': False,
        'continuedl': True,
        'sleep_interval': 5,
        'extract_audio': True,
        'audioformat': 'mp3',
        'extractor_args': {
            'youtube': 'player_client=default,-web,-web_safari'
        }
    }


    if os.getenv("PROXY_LINK"):
        ydl_opts["proxy"] = os.getenv("PROXY_LINK")
        
    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(
                ydl.download,
                [url]
            )
        response = output_link / f"{file_name}.mp3"
        return response
    except Exception as e:
        logging.warning(e)
        return None
