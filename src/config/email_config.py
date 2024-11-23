from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigEmail(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_config_email():
    return ConfigEmail()
