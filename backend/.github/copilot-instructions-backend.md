# AI Local Companion - Backend Copilot Instructions

## Architecture Overview

This is the backend component of a multi-service AI router system:
- **Backend**: FastAPI server with intelligent LLM routing (`backend/src/`)
- **Ollama**: Local LLM service orchestrated via Docker Compose

The core concept is **context-aware LLM routing** - different models handle different query types (code, simple, complex) based on configurable rules in `agent_config.json`.

## Key Components

### Router Architecture
- `RouterAgent` (`backend/src/agent/basic/router_agent.py`) - Main routing logic with two modes:
  - **Basic router** (preferred): Technology-agnostic, uses simple prompt-based classification for "code", "simple", or "complex"
  - **LangChain router**: Experimental option via `langchain_router_agent.py` (unstable, may be replaced with AutoGen or similar)
- Specialized agents inherit from `OllamaService`: `CodeAgent`, `FastAgent`, `GeneralAgent`
- Switch between routers via `use_langchain_router` config flag (default: false for stability)

### Configuration System
- `agent_config.json` - Runtime model assignments and router selection
- `src/config.py` - Config loading with automatic backup and defaults
- Models are mapped: `router_model` → classification, `code_model` → programming, `simple_model` → quick queries, `complex_model` → nuanced responses

### Service Communication
- All LLM calls go through `OllamaService` (`backend/src/commons/ollama_service.py`)
- Docker services communicate via container names: `http://ollama:11434`, `http://backend:8000`
- Environment variables: `OLLAMA_URL` for backend

## Development Workflows

### Local Development (Development Only)
```bash
# Start full stack with hot reload
docker-compose up --build

# Backend only (with debugpy on port 5678)
cd backend && uvicorn src.main:app --reload

# Run tests
cd backend && python -m unittest discover -s tests
```

### VS Code Task Integration
Use the predefined task "Docker Compose: Build and Up" for consistent development environment setup.

## Project-Specific Patterns

### Import Conventions
- Absolute imports from project root: `from src.config import load_config`
- Agent imports use full backend path: `from backend.src.commons.agent.code_agent import CodeAgent`

### Logging Strategy
- Centralized file logging to `backend.log` with structured messages
- Real-time log streaming via `/logs/stream` endpoint using SSE
- Debug info includes model selection and routing decisions

### Agent Implementation
- All agents inherit from `OllamaService` for consistent interface
- Router decision logic in `decide_agent()` uses explicit prompt templates
- Agent responses include both `response` and `model` for traceability

### API Patterns
- `/ask` endpoint returns `{response, model, router}` for full context
- `/config` GET/POST for runtime model switching without restart
- `/pull_model/{model_name}` streams model downloads via `StreamingResponse`

## Critical Files for Changes
- `router_agent.py` - Core routing logic and agent selection
- `main.py` - API endpoints and request handling
- `config.py` - Configuration management and defaults
- `docker-compose.yml` - Service orchestration and networking
- `agent_config.json` - Runtime model assignments

## Testing Approach
- Unit tests focus on routing decisions and agent selection
- Mock LLM responses for deterministic testing
- Integration tests validate full request flow through Docker services
- Basic router preferred for stability and technology independence
