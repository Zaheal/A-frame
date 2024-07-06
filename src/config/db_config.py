from functools import lru_cache
from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigDataBase(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DB_ECHO_LOG: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_db_settings():
    return ConfigDataBase()
