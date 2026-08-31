from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AI_SERVICE_",
        extra="forbid",
    )

    environment: Literal["development", "testing", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    request_timeout_seconds: float = Field(
        default=10.0,
        gt=0,
        le=60,
    )

    api_key: SecretStr


def load_settings() -> Settings:
    return Settings()