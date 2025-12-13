from pydub import AudioSegment
import asyncio
import os
from pathlib import Path


async def convert_ogg_to_mp3(
    file_path: Path
) -> Path:
    # if file_path.split(".")[-1] == "ogg":
    if file_path.suffix.lower() == ".ogg":
        audio = await asyncio.to_thread(
            AudioSegment.from_ogg,
            file_path
        )
        # new_file_path = ".".join(str(file_path).split(".")[:-1]) + ".mp3"
        new_file_path = file_path.with_suffix(".mp3")
        await asyncio.to_thread(
            audio.export,
            new_file_path,
            format = "mp3",
            bitrate = "128k"
        )
        
    return new_file_path