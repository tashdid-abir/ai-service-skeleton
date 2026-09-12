# AI Service Skeleton

A small, typed FastAPI service that exposes a deterministic sentiment predictor.
It is a learning project for building a production-shaped Python AI service with
separate API, schema, service, and configuration layers.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Setup

Clone the repository and enter the project directory. On this Windows machine,
create the project environment with Python's standard-library `venv` module
before synchronizing dependencies. Windows Application Control blocks the
interpreter produced by `uv venv` here.

```powershell
$py = uv python find --no-project --managed-python 3.12
& $py -m venv .venv
.\.venv\Scripts\python.exe --version
uv sync --locked
```

Create a local `.env` file from `.env.example` and provide the required values.
Do not commit `.env`, because it may contain secrets.

The project configures uv to copy packages into `.venv` rather than using its
default Windows hardlinks. This avoids OneDrive's incompatible-hardlink error.

### Repairing a blocked existing environment

If `.venv\Scripts\python.exe --version` reports that Windows Application
Control blocked the file, remove or rename only the disposable `.venv` folder,
then repeat the setup commands above. Do not use `uv venv` for this project.

## Run the API

Start the API from the project root:

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

The default deterministic provider runs without an external prediction service.
The HTTP provider is prepared for a future external model endpoint.

## Project structure

```text
src/ai_service_skeleton/
├── api/          HTTP route handlers
├── clients/      External HTTP/client adapters
├── core/         configuration and application exceptions
├── schemas/      Pydantic request and response models
├── services/     prediction contract and inference orchestration
└── main.py       FastAPI application setup
tests/            Automated test suite
```

## Quality checks

Run all configured local quality checks with:

```powershell
uv run python -m pre_commit run --all-files
```
