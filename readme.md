Notificaciones API
Notification management for authenticated users, sent by email, SMS or push notification.
Built with Python and FastAPI as a take-home challenge.

Features
_Filled in as features land (NOT-04 to NOT-11)._

How to run
Prerequisites (local development): Python 3.13 and uv.

cd backend
cp .env.example .env # PowerShell: Copy-Item .env.example .env; then set JWT_SECRET
uv sync
uv run fastapi dev app/main.py

Then open http://127.0.0.1:8000/docs. A Docker-only setup arrives in NOT-12.

How to run the tests
_Arrives in NOT-03._

Environment variables
All variables are listed in backend/.env.example.

Routes
Interactive documentation: /docs (Swagger UI) and /redoc.

Decisions made
uv for dependencies: one tool for the Python version, the virtual environment and a lockfile.
Typed settings that fail fast: missing configuration stops the app at startup instead of failing later.
Pre-commit with the project's own Ruff: the same linter version locally and in CI.
Areas to improve
_Filled in before delivery (NOT-14)._

Technologies
Python 3.13 · FastAPI · pydantic-settings · Ruff · pre-commit

Author
Ruben · [LinkedIn](https://www.linkedin.com/in/rubenmejia77/) · [GitHub](https://github.com/RubenMejia)