from .sc_funcs.search import search_for_music
from extra_confs.get_countries_list import countries
from settings.cache_settings import redis_client_top
from .tops_funcs.get_tops import get_top_by_country
import json
import logging


async def add_country_to_cache():
    for i in countries:
        top_country_data = await redis_client_top.get(i)
        if top_country_data:
            continue
        else:
            top = await get_top_by_country(country = i)
            top_countries_json = []
            for j in top.get("track", dict()):
                if j.get("name", None):
                    track_data = await search_for_music(
                        search_data = j.get("name"),
                        max_results = 1
                    )
                    track_data = track_data[0]
                    
                    await redis_client_top.set(
                        f"track_{track_data.get('id', 'null')}",
                        json.dumps(track_data),
                        ex = 60 * 60 * 24 * 2
                    )
                    top_countries_json.append(track_data)

            await redis_client_top.set(
                i,
                json.dumps(top_countries_json),
                ex = 60 * 60 * 24
            )
            break