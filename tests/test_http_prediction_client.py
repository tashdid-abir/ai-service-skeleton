import json

import httpx2 as httpx
import pytest

from ai_service_skeleton.clients.http_prediction_client import (
    HttpPredictionClient,
)


def test_http_prediction_client_returns_prediction() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/predict"

        request_body = json.loads(request.content)
        assert request_body == {
            "text": "This product is excellent",
        }

        return httpx.Response(
            status_code=200,
            json={
                "label": "positive",
                "confidence": 0.9,
            },
            request=request,
        )

    transport = httpx.MockTransport(handler)

    client = HttpPredictionClient(
        base_url="https://prediction.example",
        timeout_seconds=10.0,
        transport=transport,
    )

    prediction = client.predict("This product is excellent")

    assert prediction.label == "positive"
    assert prediction.confidence == 0.9


def test_http_prediction_client_propagates_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout(
            "External prediction service timed out.",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    client = HttpPredictionClient(
        base_url="https://prediction.example",
        timeout_seconds=10.0,
        transport=transport,
    )

    with pytest.raises(httpx.ReadTimeout):
        client.predict("This product is excellent")
