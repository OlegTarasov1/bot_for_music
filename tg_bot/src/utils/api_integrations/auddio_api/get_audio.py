from aiohttp import ClientSession
from aiohttp.formdata import FormData
import asyncio
import logging
import os



async def get_json_by_audio(
    audio_link: str
) -> dict:
    """Функция для получения json данных о треке по ссылке на трек в файловой системе"""

    form = FormData()

    form.add_fields(
        ("return", "apple_music,spotify"),
        ("api_token", os.getenv("AUDDIO_TOKEN"))
    )

    with open(audio_link, "rb") as file:
        binary_data = file.read()

    form.add_field(
        name = "file",
        value = binary_data, 
        filename = "audio",
        content_type = "audio/mpeg"
    )

    async with ClientSession() as session:
        async with session.post('https://api.audd.io/', data=form) as response:
            try:
                result = await response.json()
                logging.warning(f"auddio response: {result}")
            except:
                result = {}

    return result



