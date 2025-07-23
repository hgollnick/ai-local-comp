# AI Local Comp Backend: Copilot Instructions

## Overview
This repository contains a FastAPI-based backend service designed for AI-powered local computing with Ollama integration. The architecture is modular, with clear separation of concerns across API, core, models, schemas, and services layers.

## Key Architectural Components
- **API Layer (`app/api/`)**: Defines endpoints and routing logic. Organized by version (e.g., `v1`).
- **Core (`app/core/`)**: Handles configuration and logging. Key file: `config.py`.
- **Models (`app/models/`)**: Contains Pydantic models for data validation and serialization.
- **Schemas (`app/schemas/`)**: Defines request and response schemas for API endpoints.
- **Services (`app/services/`)**: Implements business logic and integrates with external dependencies like Ollama.

## Developer Workflows

### Running the Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in `.env` (see `README.md` for details).
3. Run the application:
   ```bash
   python main.py
   ```

### Running Tests
- Install development dependencies:
  ```bash
  pip install pytest pytest-asyncio httpx
  ```
- Run tests:
  ```bash
  pytest
  ```
- Run tests with coverage:
  ```bash
  pytest --cov=app tests/
  ```

### Code Quality
- Format code:
  ```bash
  black app/ tests/
  ```
- Lint code:
  ```bash
  flake8 app/ tests/
  ```
- Type checking:
  ```bash
  mypy app/
  ```

### Docker Deployment
- Build the Docker image:
  ```bash
  docker build -t ai-local-comp-backend .
  ```
- Run the container:
  ```bash
  docker run -p 8000:8000 \
    -e OLLAMA_URL=http://host.docker.internal:11434 \
    ai-local-comp-backend
  ```

## Project-Specific Conventions
- **Environment Variables**: Configuration is managed via `.env` files. Key variables include `OLLAMA_URL` and `DEBUG`. For debugging, use the `.env.debug` file, which includes settings like `LOG_LEVEL=DEBUG`.
- **Logging**: Structured logging is implemented in `app/core/logging.py`. Additionally, the `debug.py` script provides utilities for setting up and running the application in a debug environment.

## Integration Points
- **Ollama**: The backend integrates with Ollama for AI model interactions. Ensure the required models (e.g., `phi`, `codellama`, `mistral`, `llama3`) are available in Ollama.
- **Health Checks**: The `/api/v1/health` endpoint provides a health status of the service.

## Examples
- **Adding a New API Endpoint**:
  1. Create a new file in `app/api/v1/` (e.g., `new_endpoint.py`).
  2. Define the route and logic using FastAPI decorators.
  3. Import and include the router in `app/api/v1/router.py`.

- **Adding a New Service**:
  1. Create a new file in `app/services/` (e.g., `new_service.py`).
  2. Implement the business logic.
  3. Import and use the service in the relevant API endpoint or other services.

Refer to the `README.md` for additional details and examples.
