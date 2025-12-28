from extra_funcs.filler_logic import add_country_to_cache
from settings.cache_settings import redis_client_broker, redis_config_broker
from celery.schedules import crontab
import logging
from celery import Celery
import asyncio


app = Celery(
    "beat",
    broker = redis_config_broker.url,
    backend = redis_config_broker.url
)


@app.task
def fill_cache():
    asyncio.run(
        add_country_to_cache()
    )

app.conf.beat_schedule = {
    "fill_cache_periodically": {
        "task": f"{__name__}.fill_cache",
        "schedule": crontab(
            minute='*/5'
        )
    }
}


