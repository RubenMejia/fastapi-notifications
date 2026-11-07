import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2] # app/core/config.py -> backend/
ENV_FILE = BACKEND_DIR / (".env.test" if os.getenv("APP_ENV") == "test" else ".env") # backend/.env.test or backend/.env depending on the APP_ENV environment variable, which is set in the .env file

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore") # extra="ignore" means that any extra environment variables that are not defined in the Settings class will be ignored

    app_env: str = "dev"
    database_url: str # required on purpose: not default
    jwt_secret: str # required on purpose: not default
    jwt_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"] # allow requests from the frontend

settings = Settings() # this is a singleton instance of the Settings class, which is used to access the configuration settings

