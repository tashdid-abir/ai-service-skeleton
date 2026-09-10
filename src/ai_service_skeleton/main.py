import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ai_service_skeleton.api import health, prediction
from ai_service_skeleton.core.exception import (
    InvalidPredictionResultError,
    PredictionExecutionError,
)

app = FastAPI(
    title="AI Service Skeleton",
    version="0.1.0",
)


@app.exception_handler(PredictionExecutionError)
def handle_prediction_execution_error(
    _request: Request,
    exc: PredictionExecutionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(InvalidPredictionResultError)
def handle_invalid_prediction_result_error(
    _request: Request,
    exc: InvalidPredictionResultError,
) -> JSONResponse:
    return JSONResponse(
        status_code=502,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(Exception)
def handle_unexpected_error(
    _request: Request,
    _exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred.",
        },
    )


app.include_router(health.router)
app.include_router(prediction.router)


def main() -> None:
    uvicorn.run(
        "ai_service_skeleton.main:app",
        host="127.0.0.1",
        port=8000,
    )
