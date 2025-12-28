from yt_dlp import YoutubeDL 
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
            return info
        except Exception as e:
            logging.error(e)
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
