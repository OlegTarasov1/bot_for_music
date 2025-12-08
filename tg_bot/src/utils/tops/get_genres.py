from settings.cache_settings import redis_client
from httpx import AsyncClient
import logging
import json
import os


async def get_genres(
    limit: int = 20
) -> list[str]:
    list_tracks = [
        "HipHop",
        "Trap",
        "Rock",
        "House",
        "Pop",
        "Electronic",
        "Dubstap",
        "Rap",
    ]

    return list_tracks
    # genres = await redis_client.get("top_genres")


    # if genres:
    #     genres = genres.replace('"', '')
    #     genres = genres.strip("[]")
    #     genres = genres.split(", ")
    #     return genres
    # else:
    #     params = {
    #         "method": "chart.gettoptags",
    #         "api_key": os.getenv("LASTFM_TOKEN"),
    #         "format": "json",
    #         "limit": limit 
    #     }
    #     response_json = None

    #     async with AsyncClient() as client:
    #         response = await client.get(
    #             url = "http://ws.audioscrobbler.com/2.0/",
    #             params = params
    #         )
    #     response_json = response.json()
    #     response_json = response_json.get('tags', dict()).get("tag", None)

    #     response_list = [i.get("name", None) for i in response_json if "name" in i]
    #     await redis_client.set(
    #         "top_genres",
    #         json.dumps(response_list),
    #         ex = 60*60*24
    #     )

    #     if response_json:
    #         return response_list
    #     else:
    #         return None


