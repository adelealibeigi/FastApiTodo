# Todo API

A Todo API built with FastAPI following Clean Architecture principles and Domain-Driven Design concepts.

## Features

* FastAPI
* Clean Architecture
* Dependency Injection
* JWT Authentication & Authorization
* PostgreSQL Database
* SQLAlchemy ORM
* Alembic Database Migrations
* Repository Pattern
* Docker & Docker Compose
* Celery Background Tasks
* Custom Exception Handling
* Centralized Logging
* Unit Tests
* Load Testing with Locust

## Architecture

The project follows Clean Architecture to separate business logic from infrastructure concerns.


## Getting Started

### Clone Repository

```bash
git clone https://github.com/adelealibeigi/FastApiTodo.git
cd FastApiTodo
```

### Environment Variables

Create a `.env` file:


### Run With Docker

```bash
docker compose up --build
```

### Apply Migrations

```bash
alembic upgrade head
```

### Run Tests

```bash
pytest
```

## Authentication

The API uses JWT authentication.

1. Register a user
2. Login
3. Receive access and refresh token
4. Access protected endpoints using:

```http
Authorization: Bearer <token>
```


