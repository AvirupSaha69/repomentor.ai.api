"""Pydantic schemas and models for User authentication and profile details."""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


def get_utc_now() -> datetime:
    """Helper to return the current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class UserBase(BaseModel):
    """Base schema containing common fields for User models."""

    email: str = Field(..., description="The user's email address")
    full_name: str = Field(..., description="The user's full name")


class UserRegister(UserBase):
    """Schema for registering a new user."""

    password: str = Field(
        ..., min_length=6, description="The user's password (min 6 characters)"
    )


class UserLogin(BaseModel):
    """Schema for user login credentials verification."""

    email: str = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")


class UserResponse(UserBase):
    """Schema returned for user responses, omitting sensitive fields."""

    id: Optional[str] = Field(
        None, alias="_id", description="MongoDB ObjectId representation"
    )
    created_at: datetime = Field(default_factory=get_utc_now)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "Arijit Roy",
                "created_at": "2026-07-07T12:00:00Z",
            }
        },
    )


class UserDB(UserBase):
    """Schema representing the user document structure stored in MongoDB."""

    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=get_utc_now)

    model_config = ConfigDict(populate_by_name=True)


class Token(BaseModel):
    """Schema representing a generated authentication access token."""

    access_token: str
    token_type: str = "bearer"
