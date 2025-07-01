# AI Local Companion

A multi-service AI assistant stack designed as a router for LLMs. This system allows users to define which large language model (LLM) is used for each context or type of query. The backend intelligently routes user questions to the most appropriate model or agent (e.g., code, fast, general, or custom) based on configurable rules, making it easy to optimize for speed, accuracy, or cost.

## Features
- **Context-aware LLM routing:** Assign specific LLM models to different query types (e.g., coding, general knowledge, complex reasoning).
- Modular agent architecture (code, fast, general, router, ollama)
- FastAPI backend with REST endpoints
- Vite/React UI
- Ollama LLM integration
- Centralized environment variable management
- Docker Compose for easy orchestration
- Unit tests for agents and API endpoints

## How It Works
- The backend uses a RouterAgent that analyzes each user prompt and decides which agent/model should handle the request.
- You can configure which LLM is used for each agent type (code, simple, complex, etc.) in the backend configuration.
- This enables flexible, context-driven LLM selection for optimal results and resource usage.

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ai-local-comp
   ```
2. Create a `.env` file at the project root (see `.env.example` if available):
   ```env
   OLLAMA_URL=http://ollama:11434
   VITE_API_TARGET=http://backend:8000
   ```
3. Build and start all services:
   ```bash
   docker-compose up --build
   ```
4. Access the UI at [http://localhost:5173](http://localhost:5173)

## Project Structure
```
ai-local-comp/
├── backend/
│   ├── src/
│   └── tests/
├── ui/
├── docker-compose.yml
├── .env
└── README.md
```

## Testing
To run backend unit tests:
```bash
cd backend
python -m unittest discover -s tests
```

## License
See `LICENSE.txt`.
