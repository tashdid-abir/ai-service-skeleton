import pytest

from ai_service_skeleton.services.predictor import DeterministicPredictor


@pytest.fixture
def predictor() -> DeterministicPredictor:
    return DeterministicPredictor()


@pytest.mark.parametrize(
    ("text", "expected_label", "expected_confidence"),
    [
        ("This product is excellent", "positive", 1.0),
        ("This product is terrible", "negative", 1.0),
        ("This product is ordinary", "neutral", 0.5),
        ("This product is GREAT!!!", "positive", 1.0),
        ("This product is good but terrible", "neutral", 0.5),
        ("This product is good good terrible", "neutral", 0.5),
    ],
)
def test_deterministic_predictor_returns_expected_prediction(
    predictor: DeterministicPredictor,
    text: str,
    expected_label: str,
    expected_confidence: float,
) -> None:
    prediction = predictor.predict(text)

    assert prediction.label == expected_label
    assert prediction.confidence == expected_confidence
