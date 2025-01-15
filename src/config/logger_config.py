from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigLogger(BaseSettings):
    LOG_LEVEL: str 
    LOG_DISABLE: bool
    LOG_PATH: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_config_logger():
    return ConfigLogger()
