# 🧱 FastAPI Project Requirements and Architecture Guidelines

This document outlines the best practices and design requirements to structure and maintain a scalable, testable, and maintainable FastAPI project.

---

## 📁 Folder Structure

Organize your FastAPI project using a **modular architecture**, separating concerns into well-defined layers.

```
myapp/
│
├── app/                    # Main application package
│   ├── api/                # API layer (routes/controllers)
│   │   ├── v1/             # Versioned APIs
│   │   │   ├── endpoints/  # Specific route files
│   │   │   │   └── users.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/               # Application-specific settings/configs
│   │   └── config.py       # Env, secrets, and app settings
│   │
│   ├── models/             # Pydantic and ORM models
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── schemas/            # Request and response schemas (DTOs)
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── services/           # Business logic layer (aka use cases)
│   │   ├── user_service.py
│   │   └── __init__.py
│   │
│   ├── repositories/       # Database access logic
│   │   ├── user_repository.py
│   │   └── __init__.py
│   │
│   ├── db/                 # Database initialization and session
│   │   ├── base.py         # SQLAlchemy base
│   │   ├── session.py      # DB session handling
│   │   └── init_db.py
│   │
│   ├── main.py             # Application entrypoint
│   └── dependencies.py     # Shared dependencies (e.g. get_db)
│
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── Dockerfile              # Containerization support
├── requirements.txt        # Production dependencies
├── dev-requirements.txt    # Dev/test dependencies
└── README.md
```

---

## 🎯 Core Principles

### ✅ Separation of Concerns

- **Routers (API)**: Handle HTTP communication.
- **Schemas**: Define how data is sent and received.
- **Services**: Implement business logic and application rules.
- **Repositories**: Encapsulate database queries.
- **Models**: Represent persistent entities (SQLAlchemy).

### ✅ Dependency Injection

Use FastAPI’s `Depends()` to manage dependencies like:
- DB sessions
- Authenticated users
- Services

### ✅ Environment Configuration

Use `pydantic.BaseSettings` in `core/config.py` to load env variables:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🧩 Design Patterns

### 1. **Repository Pattern**

Encapsulate database access in repository classes:

```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
```

### 2. **Service Layer Pattern**

Put all business rules in service classes:

```python
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_profile(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
```

### 3. **DTO (Data Transfer Object) Pattern**

Use `schemas/` to validate and serialize data:

```python
class UserCreate(BaseModel):
    name: str
    email: EmailStr
```

### 4. **Versioned API**

Structure APIs by version to support backward compatibility:

```
api/
└── v1/
    └── endpoints/
```

---

## 🧪 Testing Practices

- Use `pytest`
- Place shared test fixtures in `tests/conftest.py`
- Mock external services and use test databases
- Aim for:
  - Unit tests for service/repo logic
  - Integration tests for route and DB flow

---

## 🚀 Run Locally

```bash
uvicorn app.main:app --reload
```

## 🐳 Run with Docker

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

---

## 📌 Additional Guidelines

- Follow **PEP8** and use **Black** for formatting
- Use **type hints** extensively
- Organize imports with **isort**
- Log with **structlog** or Python’s `logging` module
- Avoid logic inside route handlers — delegate to services
- Prefer composition over inheritance

---

## ✅ Summary

This architecture promotes:
- Scalability
- Testability
- Modularity
- Team collaboration

Stick to these rules, and Copilot (and other devs) will follow your structure with ease 🚀