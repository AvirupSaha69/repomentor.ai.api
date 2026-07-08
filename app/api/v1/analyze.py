"""API routes for repository analysis endpoints."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.api.deps import get_github_service, get_gemini_service, get_mongodb_service
from app.models.analysis import RepositoryAnalysis
from app.models.github import GitHubRepoRequest
from app.services.gemini import GeminiService
from app.services.github import GitHubService
from app.services.mongodb import MongoDBService


router = APIRouter()

@router.post("/repo", response_model=RepositoryAnalysis)
async def analyze_repository(
    request: GitHubRepoRequest,
    github_service: GitHubService = Depends(get_github_service),
    gemini_service: GeminiService = Depends(get_gemini_service),
    mongodb_service: MongoDBService = Depends(get_mongodb_service)
):
    """
    Analyzes a GitHub repository:
    1. Fetches repository metadata.
    2. Downloads structure or main codebase files.
    3. Prompts Gemini for a code quality / structure review.
    4. Saves the results into MongoDB and returns them.
    """
    try:
        # 1. Fetch metadata
        repo_info = await github_service.get_repository_info(request.owner, request.repo)

        branch = request.branch or repo_info.default_branch

        # 2. Fetch root contents to understand the structure
        contents = await github_service.get_repository_contents(
            request.owner, request.repo, path="", branch=branch
        )

        # Build structure outline
        structure_outline = "\n".join(
            [f"- {item.path} ({item.type})" for item in contents]
        )

        # 3. Analyze the structure/files with Gemini
        review = await gemini_service.analyze_repository_structure(
            structure_outline=f"Directory Structure Outline:\n{structure_outline}"
        )

        # 4. Formulate DB Analysis Document
        analysis = RepositoryAnalysis(
            owner=request.owner.lower(),
            repo=request.repo.lower(),
            branch=branch.lower(),
            repo_metadata=repo_info,
            review=review,
            created_at=datetime.utcnow()
        )

        # 5. Save to Database
        inserted_id = await mongodb_service.save_analysis(analysis)
        analysis.id = inserted_id

        return analysis

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Repository analysis failed: {str(e)}"
        ) from e

@router.get("/latest", response_model=RepositoryAnalysis)
async def get_latest_repo_analysis(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    branch: Optional[str] = Query(None, description="Repository branch"),
    github_service: GitHubService = Depends(get_github_service),
    mongodb_service: MongoDBService = Depends(get_mongodb_service)
):
    """Retrieves the latest completed analysis for a given repository."""
    try:
        # Check default branch if not specified
        if not branch:
            repo_info = await github_service.get_repository_info(owner, repo)
            branch = repo_info.default_branch

        latest = await mongodb_service.get_latest_analysis(owner, repo, branch)
        if not latest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for repository {owner}/{repo} on branch {branch}"
            )
        return latest
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrieving analysis failed: {str(e)}"
        ) from e
