from fastapi import APIRouter, Depends

from ai_service_skeleton.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import DeterministicPredictor


router = APIRouter(tags=["prediction"])


def get_inference_service() -> InferenceService:
    return InferenceService(
        predictor=DeterministicPredictor(),
        predictor_id="deterministic-v1",
    )


@router.post("/predict")
def predict(
    request: PredictionRequest,
    service: InferenceService = Depends(get_inference_service),
) -> PredictionResponse:
    return service.predict(request)