from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseSettings(BaseSettings):
    
    PG_USER_NAME: str
    PG_USER_PASSWORD: str
    PG_INTERNAL_HOST: str
    PG_PORT: int = 5432
    PG_DATABASE_NAME: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.PG_USER_NAME}:{self.PG_USER_PASSWORD}@{self.PG_INTERNAL_HOST}:{self.PG_PORT}/{self.PG_DATABASE_NAME}"
        

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

db_conf = DatabaseSettings()

async_engine = create_async_engine(db_conf.url)

async_session = async_sessionmaker(async_engine)