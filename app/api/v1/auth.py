from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserRegister, UserLogin, UserResponse, Token, UserDB
from app.services.user import UserService
from app.api.deps import get_user_service, get_current_user, get_github_service
from app.core.security import create_access_token
from app.services.github import GitHubService
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserRegister,
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user in the system."""
    existing_user = await user_service.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system."
        )
    created_user = await user_service.create(user_in)
    return created_user

@router.post("/signin", response_model=Token)
async def signin_user(
    user_login: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Sign in an existing user and return a JWT access token."""
    user = await user_service.authenticate(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user["_id"])
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

class GitHubConnectRequest(BaseModel):
    code: str

@router.post("/github/connect", response_model=UserResponse)
async def connect_github_account(
    request: GitHubConnectRequest,
    current_user: UserDB = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    global_github_service: GitHubService = Depends(get_github_service)
):
    """Exchange an OAuth code for an access token and connect the GitHub account."""
    try:
        # Exchange the OAuth code
        access_token = await global_github_service.exchange_oauth_code(request.code)
        
        # Instantiate a specific service for this user to fetch their profile
        user_gh_service = GitHubService(token=access_token)
        profile = await user_gh_service.get_authenticated_user_profile()
        
        # Build the connection object
        connection_data = {
            "github_id": profile["id"],
            "username": profile["login"],
            "access_token": access_token,
            "connected_at": datetime.now(timezone.utc),
            "is_primary": len(current_user.github_connections) == 0
        }
        
        success = await user_service.add_github_connection(str(current_user.id), connection_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save GitHub connection.")
            
        # Return updated user
        updated_user = await user_service.get_by_id(str(current_user.id))
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub connection failed: {str(e)}")
