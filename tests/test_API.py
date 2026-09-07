from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_service_skeleton.api.prediction import get_inference_service
from ai_service_skeleton.clients.prediction_client import (
    FailingPredictionClient,
)
from ai_service_skeleton.main import app
from ai_service_skeleton.services.inference import InferenceService


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
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


def get_failing_inference_service() -> tuple[InferenceService, ...]:
    return (
        InferenceService(
            predictor=FailingPredictionClient(),
            predictor_id="failing-external-v1",
        ),
    )


def test_predict_returns_503_when_predictor_times_out(
    client: TestClient,
) -> None:
    app.dependency_overrides[get_inference_service] = (
        get_failing_inference_service
    )

    response = client.post(
        "/predict",
        json={"text": "This product is excellent"},
    )

    assert response.status_code == 503
    assert "failed to produce a prediction" in response.json()["detail"]