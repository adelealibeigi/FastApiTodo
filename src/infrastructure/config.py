from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    JWT_SECRET_KEY: str
    REDIS_URL: str
    DEBUG: bool = Field(default=True)
    CELERY_BROKER_URL: str = Field(default='redis://redis:6379/3')
    CELERY_BACKEND_URL: str = Field(default='redis://redis:6379/3')
    API_HOST: str = Field(default='0.0.0.0')
    API_PORT: int = Field(default=8000)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()
