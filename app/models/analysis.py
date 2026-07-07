from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.github import GitHubRepoResponse
from app.models.gemini import GeminiCodeReview

class RepositoryAnalysis(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId representation")
    owner: str
    repo: str
    branch: str
    repo_metadata: GitHubRepoResponse
    review: GeminiCodeReview
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "owner": "octocat",
                "repo": "hello-world",
                "branch": "master",
                "repo_metadata": {
                    "owner": "octocat",
                    "repo": "hello-world",
                    "default_branch": "master",
                    "description": "My first repository",
                    "url": "https://github.com/octocat/hello-world",
                    "stars": 1500,
                    "forks": 300
                },
                "review": {
                    "summary": "The repository is simple and clean.",
                    "overall_score": 9,
                    "issues": []
                },
                "created_at": "2026-07-07T12:00:00Z"
            }
        }
    )

