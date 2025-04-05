from pydantic_settings import BaseSettings

from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class Settings(BaseSettings):
    APP_NAME: str = "Tron MS"
    VERSION: str = "v0.0.1"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    DB_HOST: str = config("DB_HOST")
    DB_PORT: int = config("DB_PORT")
    DB_NAME: str = config("DB_NAME")
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = config("DB_PASSWORD")


settings = Settings()

def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_NAME}"
    )

DATABASE_URL: str = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)
