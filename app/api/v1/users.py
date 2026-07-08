from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserDB, GitHubConnectionResponse
from app.services.user import UserService
from app.api.deps import get_current_user, get_user_service

router = APIRouter()

@router.get("/me/github", response_model=List[GitHubConnectionResponse])
async def get_github_connections(
    current_user: UserDB = Depends(get_current_user)
):
    """Get a list of connected GitHub accounts for the authenticated user."""
    # The response_model will automatically filter out access_tokens
    return current_user.github_connections

@router.delete("/me/github/{github_username}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_github_account(
    github_username: str,
    current_user: UserDB = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Disconnect a specific GitHub account from the user's profile."""
    # Check if the connection exists
    connection_exists = any(
        c.username.lower() == github_username.lower() 
        for c in current_user.github_connections
    )
    
    if not connection_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"GitHub account '{github_username}' is not connected."
        )

    success = await user_service.remove_github_connection(str(current_user.id), github_username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove GitHub connection."
        )
