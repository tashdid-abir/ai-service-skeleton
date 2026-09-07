from fastapi import APIRouter, Depends

from ai_service_skeleton.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import DeterministicPredictor

from ai_service_skeleton.clients.prediction_client import (
    FakePredictionClient,
    FailingPredictionClient
)


router = APIRouter(tags=["prediction"])


def get_inference_service() -> tuple[InferenceService, ...]:
    return (
        InferenceService(
            predictor=DeterministicPredictor(),
            predictor_id="deterministic-v1",
        ),
        InferenceService(
            predictor=FakePredictionClient(),
            predictor_id="fake-external-v1",
        ),
        InferenceService(
            predictor=FailingPredictionClient(),
            predictor_id="failing-external-v1",
        ),
    )

@router.post("/predict")
def predict(
    request: PredictionRequest,
    services: tuple[InferenceService, ...] = Depends(get_inference_service),
) -> PredictionResponse:
    return services[0].predict(request)