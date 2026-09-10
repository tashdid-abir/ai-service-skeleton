# AI Service Skeleton

A small, typed FastAPI service that exposes a deterministic sentiment predictor.
It is a learning project for building a production-shaped Python AI service with
separate API, schema, service, and configuration layers.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Setup

Clone the repository, enter the project directory, and create the locked local
environment:

```powershell
uv sync
```

Create a local `.env` file from `.env.example` and provide the required values.
Do not commit `.env`, because it may contain secrets.

## Run the API

Start the development server from the project root:

```powershell
uv run ai-service-skeleton
```

The API is then available at `http://127.0.0.1:8000`. Interactive OpenAPI
documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

### Health check

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"
```

Expected response:

```json
{
  "status": "ok"
}
```

### Prediction

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/predict" `
  -ContentType "application/json" `
  -Body '{"text":"This product is excellent"}'
```

Example response:

```json
{
  "label": "positive",
  "confidence": 1.0,
  "predictor_id": "deterministic-v1"
}
```

`POST /predict` validates its JSON body before calling the inference service.
Empty, whitespace-only, numeric-only, or overly long text receives a validation
error response.

## Project structure

```text
src/ai_service_skeleton/
├── api/          HTTP route handlers
├── core/         configuration and application exceptions
├── schemas/      Pydantic request and response models
├── services/     prediction contract and inference orchestration
└── main.py       FastAPI application setup
```
