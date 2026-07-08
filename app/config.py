import os
from typing import Optional
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Server Configurations
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "repomentor"
    
    # External API Tokens/Keys
    GITHUB_TOKEN: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("GITHUB_TOKEN", "GITHUB_PAT_TOKEN", "GITHUB _PAT_TOKEN")
    )
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # JWT Authentication Configuration
    JWT_SECRET_KEY: str = "default_secret_key_change_me_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Load from .env file if it exists
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()
