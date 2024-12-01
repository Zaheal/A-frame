from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBot(BaseSettings):
    BOT_TOKEN: str
    BASE_SITE: str
    ADMIN_ID: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


    def get_webhook_url(self) -> str:
            return f"{self.BASE_SITE}/webhook"


@lru_cache
def get_config_bot():
    return ConfigBot()
