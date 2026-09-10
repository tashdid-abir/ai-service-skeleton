import httpx2 as httpx
import pytest
from pydantic import ValidationError

from ai_service_skeleton.clients.http_prediction_client import (
    HttpPredictionClient,
)
from ai_service_skeleton.core.exception import (
    InvalidPredictionResultError,
    PredictionExecutionError,
)
from ai_service_skeleton.schemas.prediction import PredictionRequest
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import (
    BrokenPredictor,
    DeterministicPredictor,
    InvalidPredictor,
)


def test_inference_service_returns_valid_response() -> None:
    service = InferenceService(
        predictor=DeterministicPredictor(),
        predictor_id="deterministic-v1",
    )

    response = service.predict(PredictionRequest(text="This product is excellent"))

    assert response.label == "positive"
    assert response.confidence == 1.0
    assert response.predictor_id == "deterministic-v1"


def test_inference_service_wraps_predictor_failure() -> None:
    service = InferenceService(
        predictor=BrokenPredictor(),
        predictor_id="broken-v1",
    )

    with pytest.raises(PredictionExecutionError) as exc_info:
        service.predict(PredictionRequest(text="This product is good"))

    assert "broken-v1" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, TimeoutError)


def test_inference_service_wraps_invalid_prediction_result() -> None:
    service = InferenceService(
        predictor=InvalidPredictor(),
        predictor_id="invalid-v1",
    )

    with pytest.raises(InvalidPredictionResultError) as exc_info:
        service.predict(PredictionRequest(text="This product is good"))

    assert "invalid-v1" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, ValidationError)


def test_inference_service_wraps_http_client_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout(
            "External prediction service timed out.",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    service = InferenceService(
        predictor=HttpPredictionClient(
            base_url="https://prediction.example",
            timeout_seconds=10.0,
            transport=transport,
        ),
        predictor_id="http-prediction-v1",
    )

    with pytest.raises(PredictionExecutionError) as exc_info:
        service.predict(PredictionRequest(text="This product is excellent"))

    assert "http-prediction-v1" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, httpx.ReadTimeout)
