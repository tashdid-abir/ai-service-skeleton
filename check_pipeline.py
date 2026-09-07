import traceback

from ai_service_skeleton.core.exception import (
    InvalidPredictionResultError,
    PredictionExecutionError,
)
from ai_service_skeleton.schemas.prediction import PredictionRequest
from ai_service_skeleton.services.inference import InferenceService
from ai_service_skeleton.services.predictor import (
    DeterministicPredictor,
    InvalidPredictor,
    BrokenPredictor,
    Predictor,
)


def print_heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_error_details(exc: Exception) -> None:
    print("\nFull traceback:")
    traceback.print_exc()

    print("\nApplication error:", type(exc).__name__)
    print("Application message:", exc)

    if exc.__cause__ is not None:
        print("Original error:", type(exc.__cause__).__name__)
        print("Original message:", exc.__cause__)


def main(
    title: str,
    predictor: Predictor,
    predictor_id: str,
    examples: list[str],
) -> None:
    print_heading(title)

    service = InferenceService(
        predictor=predictor,
        predictor_id=predictor_id,
    )

    for number, text in enumerate(examples, start=1):
        try:
            request = PredictionRequest(text=text)
            response = service.predict(request)
        except PredictionExecutionError as exc:
            print_error_details(exc)
            return
        except InvalidPredictionResultError as exc:
            print_error_details(exc)
            return

        print(f"\nExample {number}")
        print(f"Input: {text!r}")
        print(
            f"Result: {response.label} | "
            f"Confidence: {response.confidence} | "
            f"Predictor ID: {response.predictor_id}"
        )



main(
    title="1. HAPPY PATH",
    predictor=DeterministicPredictor(),
    predictor_id="keyword-v1",
    examples=[
        "   THIS PRODUCT IS EXCELLENT!!!   ",
        "This product is AWFUL, and TERRIBLE.",
        "This is an ordinary product; nothing special?",
        "I LOVE this AMAZING product!!!",
        "The product is GOOD, but the service is TERRIBLE.",
    ],
)

main(
    title="2. PREDICTOR EXECUTION FAILURE",
    predictor=BrokenPredictor(),
    predictor_id="broken-v1",
    examples=["This product is good"],
)

main(
    title="3. INVALID PREDICTION RESULT",
    predictor=InvalidPredictor(),
    predictor_id="invalid-v1",
    examples=["This product is good"],
)