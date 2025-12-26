from pydantic_settings import BaseSettings
from redis.asyncio import Redis
from asyncio import Semaphore


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

    @property
    def url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.VIRTUAL_DATABASE}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


redis_confs = RedisSettings(v_db = 0)
redis_confs_sql = RedisSettings(v_db = 1)
redis_config_for_request_names = RedisSettings(v_db = 2)
redis_config_broker = RedisSettings(v_db = 3)

# Клиент для топов (ну так исторически сложилось уже...) 
redis_client = Redis(**redis_confs.conf_data)

# Клиент для sql запросов
redis_client_sql = Redis(**redis_confs_sql.conf_data)

# Клиент для топов
redis_client_top = Redis(**redis_config_for_request_names.conf_data)

# Клиент для брокера
redis_client_broker = Redis(**redis_config_broker.conf_data)

# Семафоры

requests_semaphore = Semaphore(1)