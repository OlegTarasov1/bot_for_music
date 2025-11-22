from yt_dlp import YoutubeDL
import asyncio


async def search_for_music(
    search_data: str,
    max_results: int = 10
) -> dict | None:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True
    }
    search_query = f"scsearch{max_results}:{search_data}"

    with YoutubeDL(ydl_opts) as ydl:
        result = await asyncio.to_thread(ydl.extract_info(search_query, download = False))
        if "entries" in result:
            return result["entries"]
        else:
            return None
