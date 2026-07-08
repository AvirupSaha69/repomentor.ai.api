"""Pydantic models for GitHub API request and response schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class GitHubRepoRequest(BaseModel):

    """Request model for specifying a GitHub repository to analyze."""

    owner: str = Field(..., description="The owner of the GitHub repository")
    repo: str = Field(..., description="The name of the repository")
    branch: Optional[str] = Field(
        None,
        description="Branch to analyze. Defaults to the repository's default branch.",
    )


class GitHubBranchInfo(BaseModel):
    """Model representing basic information about a GitHub branch."""

    name: str
    sha: str


class GitHubRepoResponse(BaseModel):
    """Response model containing metadata for a GitHub repository."""

    owner: str
    repo: str
    default_branch: str
    description: Optional[str] = None
    url: str
    stars: int
    forks: int


class GitHubFileItem(BaseModel):
    """Model representing a single file or directory entry in a GitHub repository."""

    path: str
    type: str  # "file" or "dir"
    sha: str
    size: Optional[int] = None
    url: str
    download_url: Optional[str] = None
