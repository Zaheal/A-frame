from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigRedis(BaseSettings):
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_PORT: str
    REDIS_HOST: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


@lru_cache
def get_redis_settings():
    return ConfigRedis()
