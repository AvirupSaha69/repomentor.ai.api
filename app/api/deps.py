"""FastAPI dependency injection providers for application services."""
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.services.gemini import GeminiService
from app.services.github import GitHubService
from app.services.mongodb import MongoDBService


def get_github_service() -> GitHubService:
    """Dependency injector for GitHub API Service."""
    return GitHubService()


def get_gemini_service() -> GeminiService:
    """Dependency injector for Gemini API Service."""
    return GeminiService()


def get_mongodb_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> MongoDBService:
    """Dependency injector for MongoDB Service."""
    return MongoDBService(db)
