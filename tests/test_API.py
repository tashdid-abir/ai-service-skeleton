from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_service_skeleton.api.prediction import get_inference_service
from ai_service_skeleton.clients.prediction_client import (
    FailingPredictionClient,
)
from ai_service_skeleton.main import app
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import InvalidPredictor


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def non_raising_client() -> Iterator[TestClient]:
    app.dependency_overrides.clear()

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_prediction_for_valid_input(
    client: TestClient,
) -> None:
    response = client.post(
        "/predict",
        json={"text": "This product is excellent"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["label"] == "positive"
    assert body["confidence"] == 1.0
    assert body["predictor_id"] == "deterministic-v1"


def test_predict_rejects_whitespace_only_text(
    client: TestClient,
) -> None:
    response = client.post(
        "/predict",
        json={"text": "   "},
    )

    assert response.status_code == 422


def get_failing_inference_service() -> InferenceService:
    return InferenceService(
        predictor=FailingPredictionClient(),
        predictor_id="failing-external-v1",
    )


def test_predict_returns_503_when_predictor_times_out(
    client: TestClient,
) -> None:
    app.dependency_overrides[get_inference_service] = get_failing_inference_service

    response = client.post(
        "/predict",
        json={"text": "This product is excellent"},
    )

    assert response.status_code == 503
    assert "failed to produce a prediction" in response.json()["detail"]
    assert "cause" not in response.json()


def get_invalid_inference_service() -> InferenceService:
    return InferenceService(
        predictor=InvalidPredictor(),
        predictor_id="invalid-prediction-v1",
    )


def test_predict_returns_502_for_invalid_prediction_result(
    client: TestClient,
) -> None:
    app.dependency_overrides[get_inference_service] = get_invalid_inference_service

    response = client.post(
        "/predict",
        json={"text": "This product is excellent"},
    )

    assert response.status_code == 502
    assert "returned invalid prediction data" in response.json()["detail"]
    assert "cause" not in response.json()


def get_unexpected_failure_service() -> InferenceService:
    raise RuntimeError("Unexpected internal failure.")


def test_predict_returns_safe_500_for_unexpected_error(
    non_raising_client: TestClient,
) -> None:
    app.dependency_overrides[get_inference_service] = get_unexpected_failure_service

    response = non_raising_client.post(
        "/predict",
        json={"text": "This product is excellent"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An unexpected server error occurred.",
    }
