import pytest
from pydantic import SecretStr, ValidationError

from ai_service_skeleton.core.config import Settings


def test_settings_default_to_deterministic_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(
        "AI_SERVICE_PREDICTION_PROVIDER",
        raising=False,
    )
    monkeypatch.delenv(
        "AI_SERVICE_PREDICTION_BASE_URL",
        raising=False,
    )

    settings = Settings(  # type: ignore[call-arg]
        _env_file=None,
        api_key=SecretStr("test-api-key"),
    )

    assert settings.prediction_provider == "deterministic"
    assert settings.prediction_base_url is None


def test_http_provider_requires_base_url() -> None:
    for base_url in (None, ""):
        with pytest.raises(ValidationError) as exc_info:
            Settings(  # type: ignore[call-arg]
                _env_file=None,
                api_key=SecretStr("test-api-key"),
                prediction_provider="http",
                prediction_base_url=base_url,
            )

        assert "prediction_base_url is required" in str(exc_info.value)


def test_http_provider_accepts_base_url() -> None:
    settings = Settings(  # type: ignore[call-arg]
        _env_file=None,
        api_key=SecretStr("test-api-key"),
        prediction_provider="http",
        prediction_base_url="https://prediction.example",
    )

    assert settings.prediction_provider == "http"
    assert settings.prediction_base_url == "https://prediction.example"
