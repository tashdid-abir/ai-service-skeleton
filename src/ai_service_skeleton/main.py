from fastapi import FastAPI

from ai_service_skeleton.api import health, prediction


app = FastAPI(
    title="AI Service Skeleton",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(prediction.router)