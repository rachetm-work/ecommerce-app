import os
from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "E-Commerce App"
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    DEBUG: bool = os.getenv("DEBUG", False)
    DB_DRIVER: str = os.getenv("DB_DRIVER", 'postgresql')
    DB_HOST: str = os.getenv("DB_HOST", 'localhost')
    DB_PORT: str = os.getenv("DB_PORT", '5432')
    DB_USERNAME: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME", 'ecommerce')

    # Cors Settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", ["*"])

    # Base URL Prefix
    BASE_URL_PREFIX: str = f"/api/{API_VERSION}"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
