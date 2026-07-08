"""Service module for interacting with the GitHub REST API."""

from typing import List, Optional

import httpx

from app.config import settings
from app.models.github import GitHubRepoResponse, GitHubFileItem


class GitHubService:
    """Provides methods to fetch repository info, contents, and file data from GitHub."""

    def __init__(self):
        """Initialize the GitHub API service."""
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RepoMentor-API"
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    async def get_repository_info(self, owner: str, repo: str) -> GitHubRepoResponse:
        """Fetch metadata for a given GitHub repository."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()

            return GitHubRepoResponse(
                owner=owner,
                repo=repo,
                default_branch=data.get("default_branch", "main"),
                description=data.get("description"),
                url=data.get("html_url"),
                stars=data.get("stargazers_count", 0),
                forks=data.get("forks_count", 0)
            )

    async def get_repository_contents(
        self, owner: str, repo: str, path: str = "", branch: Optional[str] = None
    ) -> List[GitHubFileItem]:
        """Fetch list of files/directories at a specific path in the repository."""
        params = {}
        if branch:
            params["ref"] = branch

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            # GitHub API can return a list or dict depending on whether path is directory or file
            if not isinstance(data, list):
                data = [data]

            return [
                GitHubFileItem(
                    path=item["path"],
                    type=item["type"],
                    sha=item["sha"],
                    size=item.get("size"),
                    url=item["url"],
                    download_url=item.get("download_url")
                )
                for item in data
            ]

    async def get_file_content(self, download_url: str) -> str:
        """Fetch the raw contents of a file via its download URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(download_url, headers=self.headers)
            response.raise_for_status()
            return response.text
