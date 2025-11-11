from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    
    PG_USER_NAME: str
    PG_USER_PASSWORD: str
    PG_INTERNAL_HOST: str
    PG_EXTERNAL_PORT: int
    PG_DATABASE_NAME: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.PG_USER_NAME}:{self.PG_USER_PASSWORD}@{self.PG_INTERNAL_HOST}:{self.PG_EXTERNAL_PORT}/{self.PG_DATABASE_NAME}"
        

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
