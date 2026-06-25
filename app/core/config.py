from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    APP_NAME: str = "AI Paraphraser"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"

    # Database
    DATABASE_URL: str | None

    # Auth
    JWT_SECRET_KEY: str | None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Rate limiting
    RATE_LIMIT: int = 1

    # Google
    OAUTH_CLIENT_ID: str | None = None
    GEMINI_API_KEY: str | None = None

    # Resend
    RESEND_API_KEY: str | None = None

    # Recaptcha
    RECAPTCHA_SECRET: str | None = None

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()