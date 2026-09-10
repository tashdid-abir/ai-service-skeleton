class ApplicationError(Exception):
    """Base class for recognized application failures."""


class PredictionError(ApplicationError):
    """Base class for failures during prediction."""


class PredictionExecutionError(PredictionError):
    """Raised when the predictor cannot complete its operation."""

    def __init__(self, predictor_id: str) -> None:
        super().__init__(f"Predictor '{predictor_id}' failed to produce a prediction.")


class InvalidPredictionResultError(PredictionError):
    """Raised when the predictor returns data that violates its contract."""

    def __init__(self, predictor_id: str) -> None:
        super().__init__(f"Predictor '{predictor_id}' returned invalid prediction data.")
