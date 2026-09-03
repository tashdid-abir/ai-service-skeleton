class ApplicationError(Exception):
    """Base class for recognized application failures."""


class PredictionError(ApplicationError):
    """Base class for failures during prediction."""


class PredictionExecutionError(PredictionError):
    """Raised when the predictor cannot complete its operation."""


class InvalidPredictionResultError(PredictionError):
    """Raised when the predictor returns data that violates its contract."""