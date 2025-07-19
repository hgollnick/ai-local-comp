# AI Local Comp Backend

A FastAPI-based backend service for AI-powered local computing with Ollama integration.

## Features

- **Modular Architecture**: Clean separation of concerns with services, models, and API layers
- **Multiple AI Agents**: Specialized agents for code, simple, and complex queries
- **Async/Await Support**: Fully asynchronous for better performance
- **Type Safety**: Comprehensive Pydantic models and type hints
- **Configuration Management**: Environment-based configuration with validation
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Health Monitoring**: Health checks and structured logging
- **Docker Support**: Container-ready with multi-stage builds

## Architecture

```
app/
├── api/                    # API endpoints and routing
├── core/                   # Core configuration and logging
├── models/                 # Pydantic data models
├── schemas/                # Request/response schemas
├── services/               # Business logic layer
└── main.py                 # Application entry point
```

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama running locally or accessible via network
- Required models pulled in Ollama (phi, codellama, mistral, llama3)

### Installation

1. **Clone and setup**:
   ```bash
   cd backend
   cp .env.example .env
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   Edit `.env` file with your settings:
   ```bash
   OLLAMA_URL=http://localhost:11434
   DEBUG=true
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Docker Deployment

```bash
# Build image
docker build -t ai-local-comp-backend .

# Run container
docker run -p 8000:8000 \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  ai-local-comp-backend
```

## API Endpoints

- `GET /` - Root endpoint with service info
- `GET /api/v1/health` - Health check
- `GET /api/v1/models` - List available Ollama models
- `GET /api/v1/config` - Get current configuration
- `POST /api/v1/ask` - Ask a question to AI agents
- `POST /api/v1/pull_model/{model_name}` - Pull a model from Ollama

## Configuration

The application uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama service URL |
| `ROUTER_MODEL` | `phi:latest` | Model for request routing |
| `CODE_MODEL` | `codellama:instruct` | Model for code queries |
| `SIMPLE_MODEL` | `mistral:instruct` | Model for simple queries |
| `COMPLEX_MODEL` | `llama3:instruct` | Model for complex queries |
| `LOG_LEVEL` | `INFO` | Logging level |

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### Debugging

The application supports remote debugging with debugpy when `DEBUG=true`:

```python
# VS Code launch.json
{
  "name": "Python: Remote Attach",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  }
}
```

## Services Overview

### RouterService
Routes incoming requests to appropriate specialized agents based on content analysis.

### OllamaService
Handles communication with Ollama API, including model management and text generation.

### ModelService
Manages Ollama models - listing, pulling, and validation.

### Agent Services
- **CodeAgentService**: Handles programming-related queries
- **SimpleAgentService**: Handles quick factual questions
- **ComplexAgentService**: Handles nuanced, multi-part questions

## Error Handling

The application includes comprehensive error handling:

- **Global exception handler**: Catches unhandled exceptions
- **Service-level errors**: Proper error propagation with logging
- **Validation errors**: Pydantic model validation
- **HTTP errors**: Proper HTTP status codes and error responses

## Monitoring and Logging

- **Structured logging**: JSON-formatted logs with rotation
- **Health checks**: Docker-compatible health monitoring
- **Performance metrics**: Request timing and processing stats
- **Debug support**: Remote debugging capabilities

## Migration from Old Structure

The refactored code maintains API compatibility while improving:

1. **Better separation of concerns**
2. **Async/await throughout**
3. **Proper dependency injection**
4. **Comprehensive error handling**
5. **Type safety and validation**
6. **Improved testability**
7. **Production-ready configuration**

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use type hints and proper error handling
5. Follow FastAPI best practices
