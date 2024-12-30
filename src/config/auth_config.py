from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigAuth(BaseSettings):
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str
    JWT_SECRET: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_auth_settings():
    return ConfigAuth()
