from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from bot.constants import LIMIT_PER_DAY


class Settings(BaseSettings):

    bot_token: SecretStr
    default_lang: str = 'ru'
    allowed_telegram_ids: Set[int] = set()
    photo_limit_per_day: int = LIMIT_PER_DAY
    redis_host: str = 'redis'
    redis_port: int = 6379
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

config = Settings()
