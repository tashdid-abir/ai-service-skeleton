from ai_service_skeleton.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from ai_service_skeleton.services.predictor import Predictor


class InferenceService:
    def __init__(
        self,
        predictor: Predictor,
        predictor_id: str,
    ) -> None:
        self._predictor = predictor
        self._predictor_id = predictor_id

    def predict(self, request: PredictionRequest,) -> PredictionResponse:
        prediction = self._predictor.predict(request.text)

        return PredictionResponse(
            label=prediction.label,
            confidence=prediction.confidence,
            predictor_id=self._predictor_id,
        )