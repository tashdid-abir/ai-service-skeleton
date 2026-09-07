from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ai_service_skeleton.api import health, prediction
from ai_service_skeleton.core.exception import PredictionExecutionError


app = FastAPI(
    title="AI Service Skeleton",
    version="0.1.0",
)

@app.exception_handler(PredictionExecutionError)
def handle_prediction_execution_error(
    request: Request,
    exc: PredictionExecutionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc),
            "cause": str(exc.__cause__) if exc.__cause__ else None,
        },
    )

app.include_router(health.router)
app.include_router(prediction.router)