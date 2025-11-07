# DQTimes Project - AI Coding Agent Instructions

## Project Overview
**DQTimes** is a time-series prediction microservice with a React frontend and FastAPI backend. This is an educational project (Biopark) focused on migrating a Rust library to Python and building a modern web application stack with Docker containerization.

## Architecture

### Frontend (`src/`)
- **Stack:** React 19 + Vite (SWC) + ESLint
- **Entry point:** `src/main.jsx` → `App.jsx` (currently renders Login component directly)
- **Component structure:** Feature-based folders under `src/components/`
- **Styling:** Component-scoped CSS files (e.g., `login/login.css`)
- **Note:** `index.css` is intentionally commented out in `main.jsx` - DO NOT uncomment unless explicitly requested

### Backend (`server/`)
- **Framework:** FastAPI 2.9.9 with Uvicorn
- **Architecture:** Service-oriented with Pydantic models
- **Structure:**
  - `app.py` - Main FastAPI application with route definitions
  - `models.py` - Pydantic schemas for request/response validation
  - `services/` - Business logic classes (e.g., `Minha_Classe` in `example_service.py`)
  - `requirements.txt` - Dependencies: pandas, fastapi, uvicorn
- **Current state:** Minimal API with root endpoint only; example service has performance comparison methods

## Development Workflows

### Frontend Development
```powershell
# Install dependencies
npm install

# Run dev server (localhost:5173 by default)
npm run dev

# Lint code
npm run lint

# Build for production
npm run build
```

### Backend Development
```powershell
# Navigate to server directory
cd server

# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Planned Docker Setup
Per README, the project intends to use Docker Compose for:
- React frontend container
- FastAPI backend container
- PostgreSQL database
- Redis for Celery task queuing
- **Note:** Docker files not yet present; when creating, follow conventions in README sections on Docker/Dockerfile/Docker Compose

## Code Conventions

### React/Frontend
- **Components:** Functional components with hooks (`useState`, `useCallback`)
- **Validation:** Form validation with regex patterns (see `Login.jsx` email validation)
- **Error handling:** Local state for errors with conditional rendering (`errors.email ? 'input-error' : ''`)
- **Naming:** PascalCase for components, camelCase for variables/functions
- **ESLint rules:** Ignores variables matching `^[A-Z_]` pattern for unused vars

### Python/Backend
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes/models
- **Type hints:** Use Pydantic models for all request/response data
- **Service pattern:** Business logic in service classes (not directly in routes)
- **Example:** `Minha_Classe` has methods returning Dict[str, Any] with structured responses
- **Models:** Nested Pydantic models (e.g., `Exemplo1Response` contains `ExemploTipo` dict)

### General Patterns
- **File organization:** Components have co-located CSS files with matching names
- **Import paths:** Explicit `.jsx` extensions in imports (`from './App.jsx'`)
- **Ports:** Frontend dev server defaults to Vite's port, backend uses 8000

## Integration Points
- Frontend currently has NO API integration (Login is client-side only with `alert()`)
- When connecting frontend to backend:
  - Use Vite proxy config OR CORS middleware in FastAPI
  - Backend runs on `http://localhost:8000` by default
  - Current backend has no authentication endpoints yet

## Key Files & Locations
- **Frontend entry:** `src/main.jsx` (React root render)
- **Backend entry:** `server/app.py` (FastAPI app instance)
- **Models:** `server/models.py` (Pydantic schemas)
- **Services:** `server/services/example_service.py` (business logic)
- **Config:** `vite.config.js` (frontend build), `eslint.config.js` (linting)

## Common Tasks

### Adding a new React component
1. Create folder in `src/components/<feature-name>/`
2. Add `<ComponentName>.jsx` and `<component-name>.css`
3. Import with explicit `.jsx` extension
4. Use functional component pattern with hooks

### Adding a new API endpoint
1. Define Pydantic models in `server/models.py`
2. Implement business logic in `server/services/<service-name>.py`
3. Create route in `server/app.py` using decorators (`@app.get`, `@app.post`)
4. Return Pydantic model instances for automatic validation

### Testing API locally
- Use FastAPI auto-docs: `http://localhost:8000/docs` (Swagger UI)
- Or: `http://localhost:8000/redoc` (ReDoc)

## Important Notes
- **License:** GPL v3 (see LICENSE file)
- **Project context:** Educational migration project (Rust → Python library)
- **README:** Contains extensive documentation on Docker, Celery, Redis, PL/Python, Alembic - refer when implementing these features
- **Current PR:** Working on login screen feature (PR #142 on `dev` branch)
- **Empty files:** `server/services/time_series.py` exists but is empty (future implementation)

## What NOT to Do
- Do NOT uncomment `import './index.css'` in `main.jsx` (intentionally disabled)
- Do NOT create generic test/error handling code without specific project patterns
- Do NOT assume database setup - PostgreSQL integration is planned but not implemented
- Do NOT ignore Pydantic validation - all request/response data should use models

## Useful Commands Reference
```powershell
# Frontend
npm run dev          # Start dev server with hot reload
npm run build        # Production build to dist/
npm run preview      # Preview production build

# Backend  
uvicorn app:app --reload                    # Dev server with auto-reload
uvicorn app:app --host 0.0.0.0 --port 8000  # Production-like server

# Future (when Docker is set up per README)
docker-compose up -d                        # Start all services
docker-compose logs -f <service>            # View service logs
docker-compose down                         # Stop all services
```