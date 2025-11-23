from aiohttp import ClientSession



async def get_json_by_audio(
    audio_link: str
) -> dict:
    data = {
        'url': "https://audd.tech/example.mp3",
        'return': 'apple_music,spotify',
        'api_token': 'test'
    }
    try:
        async with ClientSession() as session:
            result = await session.post(
                url = 'https://api.audd.io/',
                data = data
            )
            result = await result.json()
    except:
        result = dict()

    return result



