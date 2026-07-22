from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr, PositiveInt
from typing import List, Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: PostgresDsn

    # JWT / Auth
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 30
    REFRESH_TOKEN_EXPIRE_DAYS: PositiveInt = 7
    JWT_ISSUER: str = "rcms"
    JWT_AUDIENCE: str = "rcms-api"

    # API Metadata
    APP_NAME: str = "Railway Crew Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Scheduler / Scraper
    SCRAPER_INTERVAL_MINUTES: PositiveInt = 5

    # CMS Data Sources (file paths for Excel/CSV ingestion)
    CMS_DATA_PATH: str = "data/cms_data.xlsx"
    SIGNON_DATA_PATH: str = "data/signon_data.xlsx"
    MAIN_DATA_PATH: str = "data/main_data.xlsx"
    ARCHIVE_DATA_PATH: str = "data/archive_data.xlsx"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key_min_length(cls, v: SecretStr) -> SecretStr:
        if len(v.get_secret_value()) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters long"
            )
        return v


settings = Settings()
