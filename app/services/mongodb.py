"""Service module for MongoDB operations on repository analysis data."""

from typing import List, Optional, Dict, Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.analysis import RepositoryAnalysis


class MongoDBService:
    """Provides CRUD operations for repository analyses stored in MongoDB."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["repo_analyses"]

    async def save_analysis(self, analysis: RepositoryAnalysis) -> str:
        """Saves repository analysis details to MongoDB."""
        # Convert Pydantic object to dict suitable for MongoDB
        analysis_dict = analysis.model_dump(by_alias=True)
        if "_id" in analysis_dict and analysis_dict["_id"] is None:
            del analysis_dict["_id"]

        result = await self.collection.insert_one(analysis_dict)
        return str(result.inserted_id)

    async def get_latest_analysis(
        self, owner: str, repo: str, branch: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieves the latest repository analysis from MongoDB."""
        cursor = self.collection.find({
            "owner": owner.lower(),
            "repo": repo.lower(),
            "branch": branch.lower()
        }).sort("created_at", -1).limit(1)

        results = await cursor.to_list(length=1)
        if results:
            # Map _id object to string representation
            result = results[0]
            result["_id"] = str(result["_id"])
            return result
        return None

    async def list_analyses(
        self, skip: int = 0, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Lists repository analyses with pagination."""
        cursor = self.collection.find().sort(
            "created_at", -1
        ).skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        for res in results:
            res["_id"] = str(res["_id"])
        return results
