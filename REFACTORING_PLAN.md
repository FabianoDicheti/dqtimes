# DQTimes Hexagonal Architecture Refactoring Plan

---

## Executive Summary

This document outlines a complete refactoring plan to migrate the DQTimes project from its current monolithic structure to a **Hexagonal Architecture** (Ports & Adapters pattern). The refactoring will maintain existing functionality while introducing proper separation of concerns, testability, and maintainability for educational purposes.

### Key Objectives
- ✅ Adopt Hexagonal Architecture with clear boundaries
- ✅ Implement mock business logic (time-series predictions)
- ✅ Introduce SQLite database in isolated Docker container
- ✅ Maintain existing Login UI and API endpoints
- ✅ Keep architecture simple for didactic purposes
- ❌ No new features or screens during refactoring

---

## Current State Analysis

### Frontend (React + Vite)
**Location:** `src/`
- **Tech Stack:** React 19, Vite, ESLint
- **Current Features:**
  - Login component with client-side validation
  - No API integration yet
  - Form validation (email regex, password min length)
- **Current Issues:**
  - No connection to backend
  - Missing routing
  - No state management

### Backend (FastAPI)
**Location:** `server/`
- **Tech Stack:** FastAPI 2.9.9, Uvicorn, Pydantic
- **Current Features:**
  - Minimal API with root endpoint only
  - Example service with performance comparisons
  - Pydantic models defined but underutilized
- **Current Issues:**
  - No authentication implementation
  - No database layer
  - Business logic mixed with presentation
  - No proper layering

### Business Logic Reference
**Location:** `dqtimes/app/`
- **Purpose:** Reference implementation (Rust → Python migration)
- **Key Algorithms (20+ models):**
  - `naive_bayes` - Bayesian prediction
  - `media_movel3/4/12/30` - Moving averages (3, 4, 12, 30 periods)
  - `media_suave3` - Exponentially weighted moving average
  - `sazonal_aditivo/multiplicativo` - Seasonal adjustments
  - `media_mov_dupla3/4` - Double moving averages
  - `suave_dupla3/4` - Double exponential smoothing
  - `holt_winter7` - Holt-Winters method
  - `arima` - ARIMA model
  - `media_mista` - Mixed average
  - `interpolador` - 1D/2D interpolation
- **Input/Output:**
  - Input: List of historical values + number of predictions
  - Output: List of future projections
- **Note:** This code is **reference only** - we'll create simplified mocks

### Infrastructure
- **Current:** No Docker setup implemented yet
- **Planned:** Docker Compose with PostgreSQL, Redis, Celery (per README)
- **Refactoring Target:** SQLite in Docker container (simpler for education)

---

## Target Architecture: Hexagonal (Ports & Adapters)

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│                    ┌──────────────────────┐                     │
│                    │  Login Component     │                     │
│                    │  (Future: Dashboard) │                     │
│                    └──────────┬───────────┘                     │
└───────────────────────────────┼─────────────────────────────────┘
                                │ HTTP/REST
┌───────────────────────────────▼─────────────────────────────────┐
│                    PRIMARY ADAPTERS (Input)                      │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │  REST API      │  │  GraphQL       │  │  CLI (Future)   │  │
│  │  (FastAPI)     │  │  (Optional)    │  │                 │  │
│  └────────┬───────┘  └────────────────┘  └─────────────────┘  │
└───────────┼──────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                       PRIMARY PORTS (Input)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  IAuthenticationService                                     │ │
│  │  IPredictionService                                         │ │
│  │  IUserService                                               │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────┬──────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                      DOMAIN / CORE LOGIC                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Entities:                                                   ││
│  │  - User (id, email, password_hash, created_at)              ││
│  │  - Prediction (id, user_id, input_data, result, created_at) ││
│  │  - Session (id, user_id, token, expires_at)                 ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Use Cases:                                                  ││
│  │  - LoginUseCase                                              ││
│  │  - RegisterUseCase                                           ││
│  │  - CreatePredictionUseCase                                   ││
│  │  - GetPredictionHistoryUseCase                               ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Business Rules:                                             ││
│  │  - Password validation (min 8 chars)                         ││
│  │  - Email format validation                                   ││
│  │  - Token expiration (24h)                                    ││
│  │  - Input data validation (min 3 historical values)           ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────┬──────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                    SECONDARY PORTS (Output)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  IUserRepository                                            │ │
│  │  IPredictionRepository                                      │ │
│  │  ISessionRepository                                         │ │
│  │  IPredictionEngine (Mock)                                   │ │
│  │  IPasswordHasher                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────┬──────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                   SECONDARY ADAPTERS (Output)                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  SQLite Repo    │  │  Mock Prediction │  │  Bcrypt Hasher │ │
│  │  Implementation │  │  Engine          │  │                │ │
│  └─────────────────┘  └──────────────────┘  └────────────────┘ │
└───────────┬──────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  SQLite Database (Docker Container)                          ││
│  │  - users table                                               ││
│  │  - predictions table                                         ││
│  │  - sessions table                                            ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Dependency Inversion**: Core domain depends on abstractions (ports), not concrete implementations
2. **Separation of Concerns**: Clear boundaries between layers
3. **Testability**: Business logic isolated and easily testable
4. **Simplicity**: Minimal layers for educational clarity

---

## Detailed Folder Structure

### New Backend Structure (`server/`)
```
server/
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python dependencies
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Environment variables, DB config
│   └── dependencies.py              # Dependency injection container
├── domain/                          # CORE - No external dependencies
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── user.py                  # User entity (dataclass)
│   │   ├── prediction.py            # Prediction entity
│   │   └── session.py               # Session entity
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── email.py                 # Email value object with validation
│   │   └── password.py              # Password value object
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── auth_exceptions.py       # InvalidCredentials, UserExists, etc.
│   │   └── prediction_exceptions.py # InvalidInput, InsufficientData, etc.
│   └── ports/                       # Interfaces (Abstract Base Classes)
│       ├── __init__.py
│       ├── input/                   # Primary ports
│       │   ├── __init__.py
│       │   ├── authentication_service.py
│       │   ├── prediction_service.py
│       │   └── user_service.py
│       └── output/                  # Secondary ports
│           ├── __init__.py
│           ├── user_repository.py
│           ├── prediction_repository.py
│           ├── session_repository.py
│           ├── prediction_engine.py
│           └── password_hasher.py
├── application/                     # Use Cases / Business Rules
│   ├── __init__.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── login_use_case.py
│   │   │   ├── register_use_case.py
│   │   │   └── logout_use_case.py
│   │   └── prediction/
│   │       ├── __init__.py
│   │       ├── create_prediction_use_case.py
│   │       └── get_prediction_history_use_case.py
│   └── services/                    # Service implementations (orchestration)
│       ├── __init__.py
│       ├── authentication_service_impl.py
│       ├── prediction_service_impl.py
│       └── user_service_impl.py
├── adapters/                        # External interfaces
│   ├── __init__.py
│   ├── input/                       # Primary adapters
│   │   ├── __init__.py
│   │   ├── rest/
│   │   │   ├── __init__.py
│   │   │   ├── api.py               # FastAPI router aggregator
│   │   │   ├── schemas/             # Pydantic request/response models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_schemas.py
│   │   │   │   └── prediction_schemas.py
│   │   │   └── routers/
│   │   │       ├── __init__.py
│   │   │       ├── auth_router.py
│   │   │       └── prediction_router.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── auth_middleware.py   # JWT token validation
│   └── output/                      # Secondary adapters
│       ├── __init__.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   ├── sqlite_user_repository.py
│       │   ├── sqlite_prediction_repository.py
│       │   └── sqlite_session_repository.py
│       ├── engines/
│       │   ├── __init__.py
│       │   └── mock_prediction_engine.py  # Simplified time-series mock
│       └── security/
│           ├── __init__.py
│           ├── bcrypt_hasher.py
│           └── jwt_handler.py
├── infrastructure/                  # Database, migrations, etc.
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py            # SQLite connection manager
│   │   └── schema.sql               # Database schema
│   └── migrations/                  # Manual SQL migrations (simple)
│       ├── 001_create_users.sql
│       ├── 002_create_predictions.sql
│       └── 003_create_sessions.sql
└── tests/                           # Test suite
    ├── __init__.py
    ├── unit/                        # Unit tests (domain, use cases)
    │   ├── __init__.py
    │   ├── domain/
    │   └── application/
    ├── integration/                 # Integration tests (with DB)
    │   ├── __init__.py
    │   └── repositories/
    └── e2e/                         # End-to-end tests
        ├── __init__.py
        └── test_auth_flow.py
```

### Frontend Structure (Minimal Changes)
```
src/
├── main.jsx                         # Entry point (no changes)
├── App.jsx                          # Main component (add routing)
├── components/
│   └── login/
│       ├── Login.jsx                # Update to call API
│       └── login.css
├── services/                        # NEW: API client layer
│   ├── api.js                       # Axios instance configuration
│   ├── authService.js               # Login/register API calls
│   └── predictionService.js         # Prediction API calls (future)
└── utils/                           # NEW: Utilities
    ├── validation.js                # Reusable validation functions
    └── constants.js                 # API URLs, config
```

---

## Entities & Data Models

### Domain Entities

#### User Entity
```python
@dataclass
class User:
    id: int
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
```

#### Prediction Entity
```python
@dataclass
class Prediction:
    id: int
    user_id: int
    input_data: List[float]          # Historical values
    prediction_count: int            # Number of predictions requested
    result: List[float]              # Predicted values
    model_used: str                  # e.g., "moving_average_3"
    created_at: datetime
```

#### Session Entity
```python
@dataclass
class Session:
    id: int
    user_id: int
    token: str                       # JWT token
    expires_at: datetime
    created_at: datetime
```

### Database Schema (SQLite)

```sql
-- users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- predictions table
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    input_data TEXT NOT NULL,        -- JSON array of floats
    prediction_count INTEGER NOT NULL,
    result TEXT NOT NULL,             -- JSON array of floats
    model_used TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);

-- sessions table
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
```

### API Schemas (Pydantic)

```python
# Request/Response models for REST API

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    user_id: int
    email: str

class PredictionRequest(BaseModel):
    input_data: List[float] = Field(min_items=3)
    prediction_count: int = Field(ge=1, le=100)
    model: str = "moving_average_3"  # Default model

class PredictionResponse(BaseModel):
    id: int
    result: List[float]
    model_used: str
    created_at: datetime
```

---

## Mock Business Logic Specification

### Simplified Prediction Models

Instead of implementing all 20+ complex models from `dqtimes/app/`, we'll create **3 simplified mocks** for educational purposes:

#### 1. Moving Average (3 periods)
```python
def moving_average_3(data: List[float], n_predictions: int) -> List[float]:
    """
    Simple 3-period moving average.
    Each prediction = average of last 3 values.
    """
    result = []
    extended_data = data.copy()
    
    for _ in range(n_predictions):
        last_three = extended_data[-3:]
        avg = sum(last_three) / 3
        result.append(round(avg, 2))
        extended_data.append(avg)
    
    return result
```

#### 2. Linear Trend
```python
def linear_trend(data: List[float], n_predictions: int) -> List[float]:
    """
    Simple linear extrapolation based on last two points.
    """
    if len(data) < 2:
        return [data[-1]] * n_predictions
    
    slope = data[-1] - data[-2]
    result = []
    last_value = data[-1]
    
    for i in range(1, n_predictions + 1):
        prediction = last_value + (slope * i)
        result.append(round(prediction, 2))
    
    return result
```

#### 3. Naive (Last Value)
```python
def naive(data: List[float], n_predictions: int) -> List[float]:
    """
    Simplest model: repeat the last observed value.
    """
    return [data[-1]] * n_predictions
```

### Mock Engine Interface

```python
class IPredictionEngine(ABC):
    @abstractmethod
    def predict(self, data: List[float], n: int, model: str) -> List[float]:
        pass
    
    @abstractmethod
    def list_available_models(self) -> List[str]:
        pass

class MockPredictionEngine(IPredictionEngine):
    def predict(self, data: List[float], n: int, model: str) -> List[float]:
        if len(data) < 3:
            raise InsufficientDataError("Minimum 3 historical values required")
        
        models = {
            "moving_average_3": self._moving_average_3,
            "linear_trend": self._linear_trend,
            "naive": self._naive
        }
        
        if model not in models:
            raise UnsupportedModelError(f"Model '{model}' not supported")
        
        return models[model](data, n)
    
    def list_available_models(self) -> List[str]:
        return ["moving_average_3", "linear_trend", "naive"]
```

### Why Mocks, Not Real Algorithms?

1. **Educational Focus**: Easier to understand hexagonal architecture concepts
2. **Simplicity**: No external dependencies (NumPy, SciPy, etc.)
3. **Fast Testing**: Unit tests run instantly
4. **Clear Boundaries**: Shows how to swap implementations (mock ↔ real)
5. **Scope Management**: Refactoring should not expand project scope

**Future Extension**: Real prediction engines can replace mocks by implementing the same `IPredictionEngine` interface.

---

## API Endpoints Specification

### Authentication Endpoints

#### POST /api/auth/register
**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-11-06T10:30:00Z"
}
```

**Errors:**
- `400` - Invalid email format / Password too short
- `409` - Email already registered

---

#### POST /api/auth/login
**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "email": "user@example.com"
}
```

**Errors:**
- `401` - Invalid credentials
- `400` - Missing fields

---

#### POST /api/auth/logout
**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

---

### Prediction Endpoints

#### POST /api/predictions
**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "input_data": [10.5, 12.3, 14.1, 15.8, 17.2],
  "prediction_count": 3,
  "model": "moving_average_3"
}
```

**Response (201 Created):**
```json
{
  "id": 42,
  "result": [15.7, 16.0, 16.2],
  "model_used": "moving_average_3",
  "created_at": "2025-11-06T10:35:00Z"
}
```

**Errors:**
- `400` - Insufficient data (< 3 values)
- `400` - Invalid model name
- `401` - Missing/invalid token

---

#### GET /api/predictions/history
**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (default: 10, max: 100)
- `offset` (default: 0)

**Response (200 OK):**
```json
{
  "total": 25,
  "predictions": [
    {
      "id": 42,
      "input_data": [10.5, 12.3, 14.1, 15.8, 17.2],
      "prediction_count": 3,
      "result": [15.7, 16.0, 16.2],
      "model_used": "moving_average_3",
      "created_at": "2025-11-06T10:35:00Z"
    }
  ]
}
```

---

#### GET /api/predictions/{id}
**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 42,
  "input_data": [10.5, 12.3, 14.1, 15.8, 17.2],
  "prediction_count": 3,
  "result": [15.7, 16.0, 16.2],
  "model_used": "moving_average_3",
  "created_at": "2025-11-06T10:35:00Z"
}
```

**Errors:**
- `404` - Prediction not found
- `403` - Prediction belongs to another user

---

## Docker Setup Specification

### Docker Compose Structure

```yaml
version: '3.8'

services:
  # SQLite Database Container (file-based, mounted volume)
  database:
    image: alpine:3.18
    container_name: dqtimes-database
    volumes:
      - ./data/database:/data
      - ./server/infrastructure/database/schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro
    command: tail -f /dev/null  # Keep container alive
    networks:
      - backend-network

  # Backend API (FastAPI)
  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    container_name: dqtimes-backend
    environment:
      - DATABASE_PATH=/app/data/dqtimes.db
      - JWT_SECRET=${JWT_SECRET:-dev-secret-key-change-in-production}
      - JWT_EXPIRATION_HOURS=24
      - CORS_ORIGINS=http://localhost:5173
    volumes:
      - ./data/database:/app/data
      - ./server:/app:ro  # Read-only for production
    ports:
      - "8000:8000"
    depends_on:
      - database
    networks:
      - backend-network
      - frontend-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (React + Vite)
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: dqtimes-frontend
    environment:
      - VITE_API_URL=http://localhost:8000/api
    ports:
      - "5173:5173"
    depends_on:
      - backend
    networks:
      - frontend-network
    volumes:
      - ./src:/app/src:ro
      - ./public:/app/public:ro

networks:
  backend-network:
    driver: bridge
  frontend-network:
    driver: bridge

volumes:
  database:
    driver: local
```

### Backend Dockerfile

```dockerfile
# server/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Run database migrations
RUN python -m infrastructure.database.migrate

# Expose port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json .
RUN npm ci

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### Database Initialization Script

```bash
#!/bin/bash
# server/infrastructure/database/init.sh

DB_PATH="${DATABASE_PATH:-/app/data/dqtimes.db}"

if [ ! -f "$DB_PATH" ]; then
    echo "Initializing database at $DB_PATH"
    sqlite3 "$DB_PATH" < /app/infrastructure/database/schema.sql
    echo "Database initialized successfully"
else
    echo "Database already exists at $DB_PATH"
fi
```

---

## Implementation Roadmap

### Phase 1: Foundation Setup (Week 1)
**Goal:** Establish project structure and core domain

#### Tasks:
1. **Project Restructuring**
   - [ ] Create new folder structure in `server/`
   - [ ] Move existing code to `server/legacy/` for reference
   - [ ] Initialize `__init__.py` files in all packages
   - [ ] Update `.gitignore` for new structure

2. **Domain Layer**
   - [ ] Create entity classes (User, Prediction, Session)
   - [ ] Implement value objects (Email, Password)
   - [ ] Define custom exceptions
   - [ ] Create all port interfaces (ABC classes)

3. **Infrastructure**
   - [ ] Write database schema SQL
   - [ ] Create SQLite connection manager
   - [ ] Write database initialization script

**Quality Gates:**
- ✅ All domain entities have dataclass validation
- ✅ Port interfaces have proper docstrings
- ✅ Database schema validates in SQLite CLI
- ✅ No circular dependencies in imports

---

### Phase 2: Core Business Logic (Week 2)
**Goal:** Implement use cases and mock services

#### Tasks:
1. **Use Cases**
   - [ ] Implement `LoginUseCase`
   - [ ] Implement `RegisterUseCase`
   - [ ] Implement `LogoutUseCase`
   - [ ] Implement `CreatePredictionUseCase`
   - [ ] Implement `GetPredictionHistoryUseCase`

2. **Service Implementations**
   - [ ] Implement `AuthenticationServiceImpl`
   - [ ] Implement `PredictionServiceImpl`
   - [ ] Implement `UserServiceImpl`

3. **Mock Prediction Engine**
   - [ ] Implement `moving_average_3` algorithm
   - [ ] Implement `linear_trend` algorithm
   - [ ] Implement `naive` algorithm
   - [ ] Create `MockPredictionEngine` adapter

**Quality Gates:**
- ✅ All use cases have unit tests (>80% coverage)
- ✅ Mock algorithms produce correct outputs for sample data
- ✅ Business rules (password length, email validation) enforced
- ✅ No direct dependencies on frameworks in domain/application layers

---

### Phase 3: Repository Layer (Week 3)
**Goal:** Implement database adapters

#### Tasks:
1. **Repository Implementations**
   - [ ] Implement `SQLiteUserRepository`
   - [ ] Implement `SQLitePredictionRepository`
   - [ ] Implement `SQLiteSessionRepository`

2. **Security Adapters**
   - [ ] Implement `BcryptPasswordHasher`
   - [ ] Implement `JWTHandler` (token generation/validation)

3. **Database Migrations**
   - [ ] Create migration runner script
   - [ ] Write `001_create_users.sql`
   - [ ] Write `002_create_predictions.sql`
   - [ ] Write `003_create_sessions.sql`

**Quality Gates:**
- ✅ All repositories pass integration tests with real SQLite DB
- ✅ CRUD operations work correctly
- ✅ Foreign key constraints enforced
- ✅ Transactions rollback on errors
- ✅ Password hashing is secure (bcrypt cost factor ≥ 12)
- ✅ JWT tokens expire correctly

---

### Phase 4: REST API Layer (Week 4)
**Goal:** Build FastAPI adapters

#### Tasks:
1. **Pydantic Schemas**
   - [ ] Create `auth_schemas.py` (LoginRequest, RegisterRequest, etc.)
   - [ ] Create `prediction_schemas.py` (PredictionRequest, etc.)

2. **API Routers**
   - [ ] Implement `auth_router.py` (register, login, logout)
   - [ ] Implement `prediction_router.py` (create, get, history)

3. **Middleware**
   - [ ] Implement JWT authentication middleware
   - [ ] Add CORS middleware
   - [ ] Add request logging middleware

4. **Dependency Injection**
   - [ ] Create dependency injection container
   - [ ] Configure service/repository bindings
   - [ ] Setup FastAPI dependency injection

**Quality Gates:**
- ✅ All endpoints documented in OpenAPI (Swagger)
- ✅ Proper HTTP status codes for success/error cases
- ✅ Authentication required for protected endpoints
- ✅ Request validation works (Pydantic)
- ✅ CORS configured correctly for frontend

---

### Phase 5: Frontend Integration (Week 5)
**Goal:** Connect React app to backend

#### Tasks:
1. **API Client Layer**
   - [ ] Create Axios instance with base URL
   - [ ] Implement `authService.js` (login, register, logout)
   - [ ] Implement `predictionService.js` (future use)

2. **Login Component Update**
   - [ ] Replace `alert()` with API call
   - [ ] Add loading state during authentication
   - [ ] Display server-side error messages
   - [ ] Store JWT token in localStorage
   - [ ] Redirect after successful login

3. **Utilities**
   - [ ] Extract validation logic to `validation.js`
   - [ ] Create `constants.js` for API URLs

**Quality Gates:**
- ✅ Login works end-to-end (frontend → backend → database)
- ✅ Error messages displayed correctly
- ✅ Token stored and sent in subsequent requests
- ✅ No console errors in browser
- ✅ Mobile-responsive UI

---

### Phase 6: Docker Containerization (Week 6)
**Goal:** Containerize all services

#### Tasks:
1. **Docker Configuration**
   - [ ] Create `server/Dockerfile`
   - [ ] Create `Dockerfile.frontend`
   - [ ] Create `docker-compose.yml`
   - [ ] Create `.dockerignore` files

2. **Database Setup**
   - [ ] Configure SQLite volume mounting
   - [ ] Create database initialization script
   - [ ] Test migrations in container

3. **Environment Configuration**
   - [ ] Create `.env.example` file
   - [ ] Document all environment variables
   - [ ] Setup environment variable injection

4. **Testing**
   - [ ] Test `docker-compose up` from clean state
   - [ ] Verify database persistence across restarts
   - [ ] Test frontend ↔ backend communication in Docker network

**Quality Gates:**
- ✅ `docker-compose up` starts all services successfully
- ✅ Database persists data after container restart
- ✅ Frontend can access backend via Docker network
- ✅ Health checks pass for all services
- ✅ Logs accessible via `docker-compose logs`

---

### Phase 7: Testing & Documentation (Week 7)
**Goal:** Comprehensive testing and documentation

#### Tasks:
1. **Unit Tests**
   - [ ] Test all domain entities
   - [ ] Test all use cases
   - [ ] Test value objects
   - [ ] Test mock prediction engine
   - [ ] Achieve >80% code coverage

2. **Integration Tests**
   - [ ] Test repository implementations with real DB
   - [ ] Test API endpoints with TestClient
   - [ ] Test authentication flow end-to-end

3. **E2E Tests**
   - [ ] Test full user registration → login → prediction flow
   - [ ] Test error scenarios (invalid credentials, etc.)

4. **Documentation**
   - [ ] Update README.md with new architecture
   - [ ] Document API endpoints (Swagger + Markdown)
   - [ ] Create architecture diagram
   - [ ] Write setup instructions
   - [ ] Document testing procedures

**Quality Gates:**
- ✅ Test coverage >80% for domain/application layers
- ✅ All integration tests pass
- ✅ E2E tests cover critical user flows
- ✅ README includes clear setup instructions
- ✅ API documentation is complete and accurate

---

### Phase 8: Final Review & Cleanup (Week 8)
**Goal:** Polish and prepare for merge

#### Tasks:
1. **Code Quality**
   - [ ] Run linters (ESLint, Pylint)
   - [ ] Fix all linting errors
   - [ ] Format code (Prettier, Black)
   - [ ] Remove dead code
   - [ ] Remove commented-out code

2. **Security Review**
   - [ ] Verify password hashing strength
   - [ ] Check JWT secret configuration
   - [ ] Review CORS settings
   - [ ] Audit SQL injection risks
   - [ ] Review sensitive data logging

3. **Performance**
   - [ ] Profile database queries
   - [ ] Add database indexes if needed
   - [ ] Test with larger datasets (>1000 predictions)

4. **Final Testing**
   - [ ] Run full test suite
   - [ ] Manual smoke testing
   - [ ] Test in fresh environment
   - [ ] Verify Docker setup on different machine

**Quality Gates:**
- ✅ Zero linting errors
- ✅ All tests pass
- ✅ No security vulnerabilities detected
- ✅ Application starts successfully on clean machine
- ✅ Documentation is complete and accurate

---

## Quality Assurance Strategy

### Testing Pyramid

```
                 ┌─────────────┐
                 │   E2E (5%)  │  ← Full user flows in Docker
                 └─────────────┘
              ┌──────────────────┐
              │ Integration (15%) │  ← API + DB tests
              └──────────────────┘
         ┌──────────────────────────┐
         │   Unit Tests (80%)        │  ← Domain/Use Cases
         └──────────────────────────┘
```

### Unit Testing Guidelines

**Coverage Requirements:**
- Domain entities: 100%
- Use cases: >90%
- Services: >80%
- Repositories: >70% (integration tests preferred)

**Tools:**
- `pytest` (Python)
- `pytest-cov` (coverage)
- `pytest-mock` (mocking)

**Example Test Structure:**
```python
# tests/unit/application/test_login_use_case.py

class TestLoginUseCase:
    def test_successful_login(self, mock_user_repo, mock_session_repo, mock_hasher):
        # Arrange
        use_case = LoginUseCase(mock_user_repo, mock_session_repo, mock_hasher)
        email = Email("test@example.com")
        password = "securepass123"
        
        # Act
        result = use_case.execute(email, password)
        
        # Assert
        assert result.token is not None
        assert result.user_id == 1
        mock_session_repo.create.assert_called_once()
```

### Integration Testing Guidelines

**Scope:**
- Repository ↔ Database interactions
- API ↔ Use Case interactions

**Setup:**
- Use in-memory SQLite (`:memory:`)
- Reset database before each test
- Use FastAPI `TestClient`

**Example:**
```python
# tests/integration/test_auth_flow.py

def test_register_and_login_flow(test_client, db_connection):
    # Register
    response = test_client.post("/api/auth/register", json={
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    
    # Login
    response = test_client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()
```

### Code Quality Tools

#### Python (Backend)
```bash
# Linting
pylint server/ --max-line-length=120

# Type checking
mypy server/ --strict

# Formatting
black server/ --line-length=120

# Security
bandit -r server/

# Import sorting
isort server/
```

#### JavaScript (Frontend)
```bash
# Linting
npm run lint

# Type checking (if TypeScript added)
npm run type-check

# Formatting
npx prettier --write src/
```

## Migration from Current Code

### Mapping Current to New Structure

#### Backend Services
```
OLD: server/services/example_service.py
NEW: application/services/ + adapters/output/engines/mock_prediction_engine.py

OLD: server/app.py (root endpoint only)
NEW: adapters/input/rest/routers/
```

#### Models
```
OLD: server/models.py (Pydantic)
NEW: adapters/input/rest/schemas/ (API layer)
     domain/entities/ (Core domain)
```

#### Frontend Components
```
OLD: src/components/login/Login.jsx
NEW: Same location, but updated to use authService.js
```

### Data Migration

**Note:** No existing data to migrate (project has no database yet)

### Code Reuse

**Can Reuse:**
- Login component UI/CSS
- Pydantic model patterns (adapt for schemas)
- FastAPI app initialization boilerplate

**Cannot Reuse:**
- Current service structure (not hexagonal)
- Example service logic (not relevant to time-series)

### Deprecation Plan

1. Move `server/app.py` → `server/legacy/old_app.py`
2. Move `server/services/` → `server/legacy/services/`
3. Keep `dqtimes/` folder unchanged (reference only)
4. Archive old code after Phase 8 completion

---

## Dependencies & Technology Stack

### Backend Dependencies

```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic[email]==2.5.3

# Database
aiosqlite==0.19.0  # Async SQLite for FastAPI

# Security
bcrypt==4.1.2
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.26.0  # For TestClient

# Code Quality
pylint==3.0.3
mypy==1.8.0
black==24.1.1
isort==5.13.2
bandit==1.7.6

# Utilities
python-dotenv==1.0.0  # Environment variables
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "@eslint/js": "^9.33.0",
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react-swc": "^4.0.0",
    "eslint": "^9.33.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.20",
    "globals": "^16.3.0",
    "vite": "^7.1.2"
  }
}
```

### Docker Images

```yaml
# Backend
FROM python:3.11-slim

# Frontend
FROM node:20-alpine

# Database container
FROM alpine:3.18
```

---

## Performance Considerations

### Database Optimization

1. **Indexes**
   - `users.email` (unique index for login queries)
   - `predictions.user_id` (frequent joins/filters)
   - `predictions.created_at` (for history queries)
   - `sessions.token` (authentication lookups)

2. **Query Optimization**
   - Use pagination for history queries (limit/offset)
   - Avoid N+1 queries (join users with predictions)
   - Use connection pooling (future: pgbouncer if moving to PostgreSQL)

3. **SQLite Limitations**
   - Max ~100 concurrent writes/second
   - File-based (not suitable for high concurrency)
   - **Future migration**: Move to PostgreSQL for production

### API Performance

1. **Response Times**
   - Target: <100ms for authentication
   - Target: <200ms for predictions (mock algorithms are fast)

2. **Caching** (Future Enhancement)
   - Cache JWT token validation results
   - Cache user lookups by token
   - Use Redis for session storage (instead of SQLite)

3. **Rate Limiting** (Future Enhancement)
   - 100 requests/minute per user
   - 10 predictions/minute per user

### Frontend Performance

1. **Code Splitting** (Future)
   - Lazy load components
   - Separate vendor bundles

2. **API Optimization**
   - Debounce form validation
   - Cancel pending requests on component unmount

---

## Educational Notes

### Why Hexagonal Architecture for This Project?

1. **Clear Separation**: Business logic (domain) completely isolated from frameworks
2. **Testability**: Can test core logic without FastAPI or React
3. **Flexibility**: Can swap SQLite → PostgreSQL by changing one adapter
4. **Industry Standard**: Used in enterprise applications
5. **Didactic Value**: Shows architectural patterns beyond MVC

### Hexagonal Architecture Advantages

✅ **Framework Independence**: Core logic doesn't import FastAPI/Flask  
✅ **Database Independence**: Could switch to MongoDB with no domain changes  
✅ **UI Independence**: Could add CLI without touching business logic  
✅ **Testability**: Mock all external dependencies easily  
✅ **Maintainability**: Changes in one layer don't cascade  

### Trade-offs vs. Simpler Architectures

**Pros:**
- Better for learning professional patterns
- Scales well as project grows
- Forces good design decisions

**Cons:**
- More boilerplate initially
- Steeper learning curve
- Overkill for tiny projects (<1000 LOC)

**Verdict:** Worth it for educational projects teaching software architecture.

---

## Success Criteria

### Functional Requirements

✅ User can register with email/password  
✅ User can login and receive JWT token  
✅ User can logout (invalidates token)  
✅ Authenticated user can create predictions  
✅ User can view prediction history  
✅ Predictions use mock time-series algorithms  
✅ All data persists in SQLite database  
✅ System runs in Docker containers  

### Non-Functional Requirements

✅ Test coverage >80% for core logic  
✅ API response time <200ms (95th percentile)  
✅ Zero critical security vulnerabilities  
✅ Code follows PEP 8 (Python) and ESLint (JS)  
✅ All endpoints documented in Swagger  
✅ Setup from scratch in <10 minutes  
✅ Runs on Windows, macOS, Linux (via Docker)  

### Architectural Requirements

✅ Clear hexagonal architecture layers  
✅ No circular dependencies  
✅ Domain layer has zero framework imports  
✅ Business logic fully tested without mocks  
✅ Can swap database adapter without domain changes  
✅ Can add new prediction models by implementing interface  

---

## Appendices

### A. Glossary

- **Hexagonal Architecture**: Architecture pattern with business logic at center, external dependencies at edges
- **Port**: Interface (abstract class) defining contract
- **Adapter**: Concrete implementation of a port
- **Primary Port**: Input to application (use case interface)
- **Secondary Port**: Output from application (repository interface)
- **Use Case**: Single business operation (e.g., "Login User")
- **Entity**: Core business object with identity (User, Prediction)
- **Value Object**: Immutable object without identity (Email, Password)
- **Repository**: Abstraction for data persistence
- **DTO**: Data Transfer Object (Pydantic schemas for API)

### B. Reference Materials

**Hexagonal Architecture:**
- [Alistair Cockburn - Original Article](https://alistair.cockburn.us/hexagonal-architecture/)
- [Netflix Tech Blog - Ready for Changes with Hexagonal Architecture](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)

**FastAPI:**
- [Official Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy with FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/)

**Testing:**
- [Pytest Documentation](https://docs.pytest.org/)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

### C. Future Enhancements (Post-Refactoring)

**Phase 9+ (Not in Current Scope):**

1. **Real Prediction Algorithms**
   - Implement actual time-series models from `dqtimes/`
   - Add NumPy/SciPy dependencies
   - Performance optimization with Numba/Cython

2. **Advanced Features**
   - Password reset flow
   - Email verification
   - User profiles
   - Prediction model comparison
   - Export predictions (CSV/JSON)

3. **Infrastructure**
   - Migrate SQLite → PostgreSQL
   - Add Redis for caching
   - Implement Celery for async predictions
   - Add Prometheus metrics
   - Setup CI/CD pipeline (GitHub Actions)

4. **Frontend**
   - Dashboard with charts (Chart.js/Recharts)
   - Prediction visualization
   - Mobile app (React Native)
   - Real-time updates (WebSockets)

5. **DevOps**
   - Kubernetes deployment
   - Horizontal scaling
   - Load balancing
   - Monitoring & alerting

---

## Conclusion

This refactoring plan transforms DQTimes from a basic FastAPI + React prototype into a well-architected, educational demonstration of Hexagonal Architecture. By following this 8-week roadmap with clear quality gates, the team will deliver a maintainable, testable, and extensible codebase that serves as a learning foundation for software architecture principles.

### Key Takeaways

1. **Architecture First**: Hexagonal structure enables future growth
2. **Testing is Critical**: >80% coverage ensures reliability
3. **Simplicity Wins**: Mock algorithms keep focus on architecture
4. **Docker Simplifies**: Isolated SQLite container is enough for learning
5. **Documentation Matters**: Well-documented code is educational code

### Next Steps

1. Review this plan with team/instructor
2. Setup project board (GitHub Projects/Trello) with tasks
3. Begin Phase 1: Foundation Setup
4. Weekly progress reviews against quality gates
5. Adjust timeline if needed (but not scope)

---

