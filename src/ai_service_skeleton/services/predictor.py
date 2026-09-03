from dataclasses import dataclass
from typing import Protocol

from ai_service_skeleton.schemas.prediction import PredictionLabel


@dataclass(frozen=True)
class Prediction:
    label: PredictionLabel
    confidence: float

class Predictor(Protocol):
    def predict(self, text: str) -> Prediction:
        ...

class DeterministicPredictor:
    positive_words = {
        "amazing",
        "excellent",
        "good",
        "great",
        "love",
    }

    negative_words = {
        "awful",
        "bad",
        "hate",
        "poor",
        "terrible",
    }

    def predict(self, text: str) -> Prediction:
        words = {
            word.strip(".,!?;:")
            for word in text.lower().split()
        }

        positive_score = len(words & self.positive_words)
        negative_score = len(words & self.negative_words)

        if positive_score > negative_score:
            label: PredictionLabel = "positive"
        elif negative_score > positive_score:
            label = "negative"
        else:
            label = "neutral"

        total_score = positive_score + negative_score

        if total_score == 0 or positive_score == negative_score:
            confidence = 0.5
        else:
            difference = abs(positive_score - negative_score)
            confidence = 0.5 + difference / (2 * total_score)

        return Prediction(
            label=label,
            confidence=round(confidence, 2),
        )