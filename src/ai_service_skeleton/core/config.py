from __future__ import annotations

from typing import Literal

from pydantic import Field, SecretStr, model_validator
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

    prediction_provider: Literal["deterministic", "http"] = "deterministic"

    prediction_base_url: str | None = None

    @model_validator(mode="after")
    def validate_http_prediction_settings(self) -> Settings:
        if self.prediction_provider == "http" and not self.prediction_base_url:
            raise ValueError("prediction_base_url is required when prediction_provider is 'http'")

        return self


def load_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]  # Loaded from environment/.env.
