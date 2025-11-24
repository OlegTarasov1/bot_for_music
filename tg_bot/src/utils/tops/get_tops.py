from httpx import AsyncClient
import os


async def get_top_by_country(
    country: str
) -> dict | None:
    async with AsyncClient() as client:
        response = await client.get(
            url = f"http://ws.audioscrobbler.com/2.0/",
            params = {
                "method": "geo.gettoptracks",
                "country": country,
                "limit": 50,
                "api_key": os.getenv('LASTFM_TOKEN'),
                "format": "json"
            }
        )
    
    if response.status_code == 200:
        return response.json().get("tracks", dict())
    else:
        return None


async def get_top_of_all() -> dict | None:
    params = {
        "method": "chart.gettoptracks",
        "limit": 50,
        "api_key": os.getenv("LASTFM_TOKEN"),
        "format": "json"
    }
    async with AsyncClient() as client:
        response = await client.get(
            utl = "http://ws.audioscrobbler.com/2.0/",
            params = params
        )

    if response.status_code == 200:
        return response.json()
    else:
        return None