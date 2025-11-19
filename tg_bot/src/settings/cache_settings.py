from pydantic_settings import BaseSettings
from redis.asyncio import Redis


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def conf_data(self):
        conf_data = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "decode_responses": True
        }
        return conf_data


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


redis_confs = RedisSettings()

redis_client = Redis(**redis_confs.conf_data)