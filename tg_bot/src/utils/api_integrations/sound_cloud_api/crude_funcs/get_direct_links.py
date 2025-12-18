from yt_dlp import YoutubeDL
from pathlib import Path
from uuid import uuid4
import logging
import asyncio
import os


async def get_direct_music_url(
    url: str
) -> dict:
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio/best',
        "quiet": True,
        'no_warnings': True,
        'skip_download': True
    }

    if os.getenv("PROXY_LINK"):
        ydl_opts["proxy"] = os.getenv("PROXY_LINK")

    with YoutubeDL(ydl_opts) as ydl:
        result = await asyncio.to_thread(
            ydl.extract_info,
            url,
            download = False
        )

    return result


async def get_mp3_links(
    entrie: dict[dict[str]]
) -> list[str] | None:
    links = []

    for i in entrie.get("formats", []):
        if i.get("format_id", "").startswith("http_mp3") and i.get("url", None):
            links.append(i.get("url"))

    return links


async def install_track(
    download_links: list[str]
) -> str | None:
    output_link = Path("/app/media")
    output_link.mkdir(parents = True, exist_ok = True)

    for i, value in enumerate(download_links):
        try:
            logging.warning("обработка...")
            file_name = uuid4()
            output_template = str(output_link / f"{file_name}.%(ext)s")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'quiet': False,
            }

            if os.getenv("PROXY_LINK"):
                ydl_opts["proxy"] = os.getenv("PROXY_LINK")
                
            with YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(
                    ydl.download,
                    value
                )
            
            response = output_link / f"{file_name}.mp3"
            
            return response 

        except Exception as e:
            logging.warning(e)
            continue
    return None


async def delete_file(
    filepath: str
) -> bool:
    try: 
        await asyncio.to_thread(
            os.remove,
            filepath
        )
        return True
    except Exception as e:
        logging.warning(e)
        return False




