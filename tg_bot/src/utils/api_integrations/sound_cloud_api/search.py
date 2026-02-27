from yt_dlp import YoutubeDL 
from settings.cache_settings import redis_client_track
import os
import logging
import asyncio
import json


async def search_for_music(
    search_data: str,
    max_results: int | None = 50
) -> list[dict] | None:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True
    }

    if os.getenv("PROXY_LINK"):
        ydl_opts["proxy"] = os.getenv("PROXY_LINK")

    search_query = f"scsearch{max_results if max_results else ''}:{search_data}"

    with YoutubeDL(ydl_opts) as ydl:
        result = await asyncio.to_thread(
            ydl.extract_info,
            search_query,
            download = False
        )
        if "entries" in result:
            return result["entries"]
        else:
            return None


async def get_soundcloud_track_by_id(track_id: int | str) -> dict | None:
    url = f"https://api.soundcloud.com/tracks/{track_id}"

    try:
        existant_data = await redis_client_track.get(f"track_{track_id}")
    except Exception as e:
        logging.error(e)
        return None

    if existant_data:
        existant_data = json.loads(existant_data)

        return existant_data

    else:

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        if os.getenv("PROXY_LINK"):
            ydl_opts["proxy"] = os.getenv("PROXY_LINK")

        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = await asyncio.to_thread(
                    ydl.extract_info,
                    url,
                    download=False
                )

                if info:
                    redis_client_track.set(
                        name = f"track_{track_id}",
                        value = json.dumps(info),
                        ex = 60*60 * 2 
                    )

                return info

            except Exception as e:
                print(f"Трек не найден или ошибка: {e}")
                return None



async def search_for_music_by_tag(
    search_data: str,
    max_results: int | None = 50
) -> list[dict] | None:
    logging.warning(f"searching for: {search_data} (request)")
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True
    }
    
    if os.getenv("PROXY_LINK"):
        ydl_opts["proxy"] = os.getenv("PROXY_LINK")
        
    search_query = f"scsearch{max_results if max_results else ''}:tag:{search_data}"

    with YoutubeDL(ydl_opts) as ydl:
        result = await asyncio.to_thread(
            ydl.extract_info,
            search_query,
            download = False
        )
        if "entries" in result:
            return result["entries"]
        else:
            return None
