from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigCelery(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_NUMBER_OF_WORKERS: int

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_celery_settings():
    return ConfigCelery()
