# AI Service Skeleton

A modular AI service framework providing core configurations, schema validation, client management, and REST API utilities for building scalable AI applications.

## Features

- **Core Configuration**: Centralized configuration management with environment variable support
- **Schema Validation**: Pydantic-based schema validation for data consistency
- **Client Management**: Extensible client infrastructure for service integration
- **API Utilities**: REST API building blocks for rapid service development
- **Modular Architecture**: Clean separation of concerns with independent modules

## Requirements

Python >= 3.12

## Installation

Install the package using pip:

```bash
pip install ai-service-skeleton
```

## Project Structure

```
ai-service-skeleton/
├── src/ai_service_skeleton/
│   ├── api/              # REST API utilities
│   ├── clients/          # Client management
│   ├── core/             # Core configuration
│   ├── schemas/          # Data schemas
│   └── services/         # Service implementations
├── tests/                # Test suite
├── pyproject.toml        # Project metadata
└── README.md             # This file
```

## Quick Start

```python
from ai_service_skeleton.core.config import Config

# Initialize configuration
config = Config()

# Use in your application
print(config)
```

## Development

For development setup, clone the repository and install dependencies:

```bash
uv sync
```

## License

MIT License