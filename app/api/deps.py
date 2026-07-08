from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
import jwt
from app.config import settings
from app.core.database import get_database
from app.services.mongodb import MongoDBService
from app.services.github import GitHubService
from app.services.gemini import GeminiService
from app.services.user import UserService
from app.models.user import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

def get_github_service() -> GitHubService:
    """Dependency injector for global GitHub API Service."""
    return GitHubService()

def get_gemini_service() -> GeminiService:
    """Dependency injector for Gemini API Service."""
    return GeminiService()

def get_mongodb_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> MongoDBService:
    """Dependency injector for MongoDB Service."""
    return MongoDBService(db)

def get_user_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> UserService:
    """Dependency injector for UserService."""
    return UserService(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> UserDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return UserDB(**user)

def get_user_github_service(
    github_username: Optional[str] = None,
    current_user: UserDB = Depends(get_current_user)
) -> GitHubService:
    """Dependency injector for user-specific GitHub API Service."""
    if not current_user.github_connections:
        # Fallback to global service if no connections exist
        return GitHubService()
        
    token_to_use = None
    if github_username:
        for conn in current_user.github_connections:
            if conn.username.lower() == github_username.lower():
                token_to_use = conn.access_token
                break
    else:
        # Use primary or first connection
        primary_conn = next((c for c in current_user.github_connections if c.is_primary), None)
        if primary_conn:
            token_to_use = primary_conn.access_token
        elif len(current_user.github_connections) > 0:
            token_to_use = current_user.github_connections[0].access_token

    return GitHubService(token=token_to_use)

