from pydantic_settings import BaseSettings
from redis.asyncio import Redis


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    VIRTUAL_DATABASE: int = 0

    def __init__(
            self,
            v_db = 0,
            *args,
            **kwargs
        ):
        super().__init__(
            *args,
            **kwargs
        )
        self.VIRTUAL_DATABASE = v_db

    @property
    def conf_data(self):
        conf_data = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "decode_responses": True,
            "db": self.VIRTUAL_DATABASE
        }
        return conf_data


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


redis_confs = RedisSettings()
redis_confs_sql = RedisSettings(v_db = 1)

# Клиент для топов (ну так исторически сложилось уже...) 
redis_client = Redis(**redis_confs.conf_data)

redis_client_sql = Redis(**redis_confs_sql.conf_data)