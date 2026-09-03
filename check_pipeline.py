from ai_service_skeleton.services.predictor import DeterministicPredictor
from ai_service_skeleton.services.inference import InferenceService

from ai_service_skeleton.schemas.prediction import PredictionRequest


predictor = DeterministicPredictor()

service = InferenceService(predictor=predictor, predictor_id="keyword-v1")


examples = [
    "   THIS PRODUCT IS EXCELLENT!!!   ",
    "This product is AWFUL, and TERRIBLE.",
    "This is an ordinary product; nothing special?",
    "I LOVE this AMAZING product!!!",
    "The product is GOOD, but the service is TERRIBLE.",
]

for number, text in enumerate(examples, start=1):
    request = PredictionRequest(text=text)
    response = service.predict(request)

    print(f"Example {number}")
    print(f"Input: {text!r}")
    print(
        f"Result: {response.label} | "
        f"Confidence: {response.confidence} | "
        f"Predictor ID: {response.predictor_id}"
    )
    print("-" * 60)