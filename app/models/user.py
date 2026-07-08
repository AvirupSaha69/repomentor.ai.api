from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class GitHubConnectionResponse(BaseModel):
    github_id: int = Field(..., description="The user's GitHub ID")
    username: str = Field(..., description="The user's GitHub username")
    connected_at: datetime = Field(..., description="When the account was connected")
    is_primary: bool = Field(False, description="Whether this is the primary connection")

class GitHubConnection(GitHubConnectionResponse):
    access_token: str = Field(..., description="The GitHub access token for this connection")

class UserBase(BaseModel):
    email: str = Field(..., description="The user's email address")
    full_name: str = Field(..., description="The user's full name")

class UserRegister(UserBase):
    password: str = Field(..., min_length=6, description="The user's password (min 6 characters)")

class UserLogin(BaseModel):
    email: str = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")

class UserResponse(UserBase):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId representation")
    github_connections: List[GitHubConnectionResponse] = Field(default_factory=list, description="Connected GitHub accounts")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "Arijit Roy",
                "created_at": "2026-07-07T12:00:00Z"
            }
        }
    )

class UserDB(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    github_connections: List[GitHubConnection] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True
    )

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
