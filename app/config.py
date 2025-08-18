import os

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    db_type: str = os.getenv('DB_TYPE', 'postgresql')
    db_api: str = os.getenv('DB_API', 'asyncpg')
    postgres_user: str = os.getenv('POSTGRES_USER', 'User')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'qwerty')
    db_host: str = os.getenv('DB_HOST', 'localhost')
    port_db_postgres: str = os.getenv('PORT_DB_POSTGRES', '5432')
    postgres_db: str = os.getenv('POSTGRES_DB', 'somedb')

    app_title: str = os.getenv('APP_TITLE', 'FlexSet')
    description: str = os.getenv('DESCRIPTION', 'Language learning platform')
    log_level: str = os.getenv('LOG_LEVEL', 'DEBUG')
    secret: str = os.getenv('SECRET', 'secret')
    reset_password_token_secret: str = os.getenv(
        'RESET_PASSWORD_SECRET', '123')
    verification_token_secret: str = os.getenv(
        'VERIFICATION_SECRET', '123')

    model_config = ConfigDict(env_file='.env', extra='ignore')

    @property
    def database_url(self):
        return (
            f'{self.db_type}+{self.db_api}://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.db_host}:{self.port_db_postgres}/{self.postgres_db}'
        )


settings = Settings()
