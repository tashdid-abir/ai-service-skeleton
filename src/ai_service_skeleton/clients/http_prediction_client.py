from typing import cast

import httpx2 as httpx

from ai_service_skeleton.schemas.prediction import PredictionLabel
from ai_service_skeleton.services.predictor import Prediction


class HttpPredictionClient:
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout_seconds,
            transport=transport,
        )

    def predict(self, text: str) -> Prediction:
        response = self._client.post(
            "/predict",
            json={"text": text},
        )
        response.raise_for_status()

        data = response.json()

        return Prediction(
            label=cast(PredictionLabel, data["label"]),
            confidence=float(data["confidence"]),
        )