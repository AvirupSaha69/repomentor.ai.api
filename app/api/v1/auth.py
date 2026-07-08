"""API routes for user registration and sign-in authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_service
from app.core.security import create_access_token
from app.models.user import UserRegister, UserLogin, UserResponse, Token
from app.services.user import UserService


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
