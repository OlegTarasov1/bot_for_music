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

    logging.warning(result)
    return result


async def get_mp3_links(
    entrie: dict[dict[str]]
) -> list[str] | None:
    links = []
    logging.warning(f"entries:\n{entrie}")
    for i in entrie.get("formats", []):
        if i.get("url", None):
            links.append(
                {
                    "url": i.get("url"),
                    "format_id": i.get("format_id")
                }
            )

    logging.warning(links)
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
            output_template = str(output_link / f"{file_name}.mp3")
            ydl_opts = {
                'format': 'bestaudio/best',
                'extract_audio': True,
                'audio_format': 'mp3',
                'audio_quality': 0,
                'outtmpl': output_template,
                'prefer_ffmpeg': True,
                'embed_thumbnail': True,
                'add_metadata': True,
                'noplaylist': True,
                'quiet': False,
                'postprocessor_args': [
                    '-ar', '44100',
                    '-ac', '2',
                    '-b:a', '320K',
                ],
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




