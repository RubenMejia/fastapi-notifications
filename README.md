# Notifications API

Notification management for authenticated users, sent by email, SMS or push notification.
Built with Python and FastAPI as a take-home challenge.

## Features
_Filled in as features land (NOT-04 to NOT-11)._

## How to run
**Prerequisites (local development):** Python 3.13, [uv](https://docs.astral.sh/uv/) and Docker.

    docker compose up -d db          # PostgreSQL 16 on localhost:5432
    cd backend
    cp .env.example .env             # PowerShell: Copy-Item .env.example .env; then set JWT_SECRET
    uv sync
    uv run alembic upgrade head
    uv run fastapi dev app/main.py

Then open http://127.0.0.1:8000/docs. A Docker-only setup arrives in NOT-12.

## How to run the tests

Tests run against a separate, throwaway Postgres (`notifications_test` on port 5433, kept in memory):

    docker compose -f docker-compose.test.yml up -d db_test
    cd backend
    uv run pytest

Migrations are applied at the start of the run and coverage is printed at the end.
Stop the test database with `docker compose -f docker-compose.test.yml down`.

## Environment variables
All variables are listed in `backend/.env.example`.

## Routes
Interactive documentation: `/docs` (Swagger UI) and `/redoc`.

## Decisions made
- **uv for dependencies:** one tool for the Python version, the virtual environment and a lockfile.
- **Typed settings that fail fast:** missing configuration stops the app at startup instead of failing later.
- **Pre-commit with the project's own Ruff:** the same linter version locally and in CI.
- **PostgreSQL in Docker for local development:** one command gives every developer the same database version.
- **Alembic migrations from the first table:** versioned, reversible schema changes instead of `create_all`, with a naming convention that gives every constraint a predictable name.
- **Separate test database (`notifications_test`, port 5433, in memory):** tests can never touch dev data. A guard in `tests/conftest.py` refuses any database whose name does not end in `_test`. Migrations run once per test session and every table is emptied before each test, so tests are independent and run in any order.

## Areas to improve
- A readiness check that also pings the database; today `/health` only proves the process is up.

## Technologies
Python 3.13 · FastAPI · SQLAlchemy 2.0 (async) · Alembic · PostgreSQL 16 · Docker · pydantic-settings · Ruff · pre-commit

## Author
Ruben · [LinkedIn](https://www.linkedin.com/in/rubenmejia77/) · [GitHub](https://github.com/RubenMejia)