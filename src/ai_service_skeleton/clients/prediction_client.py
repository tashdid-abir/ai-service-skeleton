from typing import Protocol

from ai_service_skeleton.services.predictor import Prediction


class PredictionClient(Protocol):
    def predict(self, text: str) -> Prediction: ...


class FakePredictionClient:
    def predict(self, text: str) -> Prediction:
        return Prediction(
            label="neutral",
            confidence=0.5,
        )


class FailingPredictionClient:
    def predict(self, text: str) -> Prediction:
        raise TimeoutError("External prediction service timed out.")
