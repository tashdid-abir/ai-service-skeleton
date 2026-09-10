from typing import Annotated

from fastapi import APIRouter, Depends

from ai_service_skeleton.clients.http_prediction_client import (
    HttpPredictionClient,
)
from ai_service_skeleton.core.config import Settings, load_settings
from ai_service_skeleton.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import (
    DeterministicPredictor,
    Predictor,
)

router = APIRouter(tags=["prediction"])


def get_settings() -> Settings:
    return load_settings()


def get_inference_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> InferenceService:
    predictor: Predictor

    if settings.prediction_provider == "http":
        base_url = settings.prediction_base_url

        if base_url is None:
            raise RuntimeError("HTTP prediction provider requires a base URL.")

        predictor = HttpPredictionClient(
            base_url=base_url,
            timeout_seconds=settings.request_timeout_seconds,
        )
        predictor_id = "http-prediction-v1"

    else:
        predictor = DeterministicPredictor()
        predictor_id = "deterministic-v1"

    return InferenceService(
        predictor=predictor,
        predictor_id=predictor_id,
    )


@router.post("/predict")
def predict(
    request: PredictionRequest,
    service: Annotated[
        InferenceService,
        Depends(get_inference_service),
    ],
) -> PredictionResponse:
    return service.predict(request)
