import pytest
from pydantic import ValidationError

from ai_service_skeleton.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)


def test_prediction_request_strips_outer_whitespace() -> None:
    request = PredictionRequest(text="   This product is excellent   ")

    assert request.text == "This product is excellent"


@pytest.mark.parametrize(
    "test_text",
    [
        "",
        "   ",
        "12345",
        "a" * 2_001,
    ],
)
def test_prediction_request_rejects_invalid_text(test_text: str) -> None:
    with pytest.raises(ValidationError):
        PredictionRequest(text=test_text)


def test_prediction_response_accepts_valid_data() -> None:
    response = PredictionResponse(
        label="positive",
        confidence=0.9,
        predictor_id="deterministic-v1",
    )

    assert response.label == "positive"
    assert response.confidence == 0.9
    assert response.predictor_id == "deterministic-v1"


@pytest.mark.parametrize(
    "test_response_data",
    [
        {
            "label": "happy",
            "confidence": 0.9,
            "predictor_id": "deterministic-v1",
        },
        {
            "label": "positive",
            "confidence": -0.1,
            "predictor_id": "deterministic-v1",
        },
        {
            "label": "positive",
            "confidence": 1.1,
            "predictor_id": "deterministic-v1",
        },
        {
            "label": "positive",
            "confidence": 0.9,
            "predictor_id": "",
        },
    ],
)
def test_prediction_response_rejects_invalid_data(
    test_response_data: dict[str, str | float],
) -> None:
    with pytest.raises(ValidationError):
        PredictionResponse.model_validate(test_response_data)
