from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBot(BaseSettings):
    TOKEN: str
    API_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_bot_settings():
    return ConfigBot()
