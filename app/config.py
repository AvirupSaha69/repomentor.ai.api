"""Application configuration loaded from environment variables and .env file."""
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings with defaults and .env overrides."""

    # API Server Configurations
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "repomentor"

    # External API Tokens/Keys
    GITHUB_TOKEN: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Load from .env file if it exists
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()
