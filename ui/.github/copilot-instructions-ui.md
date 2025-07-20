# AI Local Companion - UI Copilot Instructions

## Architecture Overview

This is the UI component of a multi-service AI router system:
- **UI**: Vite-based configuration interface (`ui/src/`)
- Planned migration from React to Angular or Svelte
- Communicates with backend and Ollama via Docker Compose networking

## Key Components

### UI Architecture
- Vite-based frontend in `ui/src/`
- Components for log viewing, model selection, Ollama URL input, etc.
- Uses environment variable `VITE_API_TARGET` for backend API proxy

### Service Communication
- UI communicates with backend via API proxy
- Docker Compose ensures service discovery via container names

## Development Workflows

### Local Development (Development Only)
```bash
# Start full stack with hot reload
docker-compose up --build
```

### VS Code Task Integration
Use the predefined task "Docker Compose: Build and Up" for consistent development environment setup.

## Project-Specific Patterns

### UI Component Patterns
- Components in `ui/src/components/` for modularity
- Planned migration from React to Angular or Svelte (update instructions as needed)

### API Patterns
- UI calls backend endpoints for config, logs, and model management
- Uses `VITE_API_TARGET` for API requests

## Critical Files for Changes
- `ui/src/` - Main UI source code
- `ui/src/components/` - UI components
- `docker-compose.yml` - Service orchestration and networking

## Testing Approach
- Manual testing via browser
- (Add automated UI tests as migration progresses)
