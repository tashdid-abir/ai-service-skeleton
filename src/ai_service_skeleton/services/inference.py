from pydantic import ValidationError

from ai_service_skeleton.core.exception import (
    InvalidPredictionResultError,
    PredictionExecutionError,
)
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

    def predict(self, request: PredictionRequest) -> PredictionResponse:

        try:
            prediction = self._predictor.predict(request.text)
        except Exception as exc:
            raise PredictionExecutionError(self._predictor_id) from exc

        try:
            return PredictionResponse(
                label=prediction.label,
                confidence=prediction.confidence,
                predictor_id=self._predictor_id,
            )
        except ValidationError as exc:
            raise InvalidPredictionResultError(self._predictor_id) from exc
