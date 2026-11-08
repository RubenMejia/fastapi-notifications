import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]  # app/core/config.py -> backend/

# backend/.env.test or backend/.env depending on the APP_ENV environment variable
ENV_FILE = BACKEND_DIR / (".env.test" if os.getenv("APP_ENV") == "test" else ".env")


class Settings(BaseSettings):
    # extra="ignore" means that any extra env var are not defined in Settings class will be ignored
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    app_env: str = "dev"
    database_url: str  # required on purpose: not default
    jwt_secret: str  # required on purpose: not default
    jwt_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]  # allow requests from the frontend

    @field_validator(
        "database_url"
    )  # this decorator is used to validate the database_url field / property.
    @classmethod  # this decorator is used to define a class method.
    def use_asyncpg_driver(cls, url: str) -> str:
        # this is a docstring. it is a string that describes the function.
        """Hosting platforms hand out postgres:// URLs; async SQLAlchemy needs asyncpg."""
        for prefix in ("postgresql+asyncpg://", "postgres://", "postgresql://"):
            if url.startswith(prefix):
                return "postgresql+asyncpg://" + url.removeprefix(prefix)
        raise ValueError("DATABASE_URL must be a PostgreSQL URL")


# this is a singleton instance of Settings class, which is used to access the configuration settings
settings = Settings()
