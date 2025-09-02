from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения и секретные данные.
    """

    app_title: str = 'Telebot-photoshop API'
    description: str = 'Telegram bot – photo background remover with color palette'
    api_version: str = '1'
    log_level: str = 'INFO'
    api_host: str = '0.0.0.0'
    api_port: int = 8000
    allowed_image_mb: int = 15

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

settings = Settings()
