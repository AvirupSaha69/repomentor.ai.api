from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GitHubRepoRequest(BaseModel):
    owner: str = Field(..., description="The owner of the GitHub repository")
    repo: str = Field(..., description="The name of the repository")
    branch: Optional[str] = Field(None, description="Branch to analyze. Defaults to the repository's default branch.")

class GitHubBranchInfo(BaseModel):
    name: str
    sha: str

class GitHubRepoResponse(BaseModel):
    owner: str
    repo: str
    default_branch: str
    description: Optional[str] = None
    url: str
    stars: int
    forks: int

class GitHubFileItem(BaseModel):
    path: str
    type: str  # "file" or "dir"
    sha: str
    size: Optional[int] = None
    url: str
    download_url: Optional[str] = None
