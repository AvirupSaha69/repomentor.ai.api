from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional
from app.models.github import GitHubRepoResponse, GitHubFileItem
from app.services.github import GitHubService
from app.api.deps import get_github_service

router = APIRouter()

@router.get("/repo", response_model=GitHubRepoResponse)
async def get_repo_details(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    github_service: GitHubService = Depends(get_github_service)
):
    """Fetch GitHub Repository basic metadata."""
    try:
        return await github_service.get_repository_info(owner, repo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch repository: {str(e)}"
        )

@router.get("/contents", response_model=List[GitHubFileItem])
async def get_repo_contents(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    path: str = Query("", description="Path in the repository"),
    branch: Optional[str] = Query(None, description="Repository branch"),
    github_service: GitHubService = Depends(get_github_service)
):
    """Fetch files or directories inside the repository path."""
    try:
        return await github_service.get_repository_contents(owner, repo, path, branch)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch contents: {str(e)}"
        )
