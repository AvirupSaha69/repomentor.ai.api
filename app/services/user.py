from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.user import UserRegister
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timezone

class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["users"]

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user document from MongoDB by email."""
        user = await self.collection.find_one({"email": email.lower()})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None

    async def create(self, user_in: UserRegister) -> Dict[str, Any]:
        """Create a new user with hashed password and save to MongoDB."""
        hashed_password = get_password_hash(user_in.password)
        
        user_dict = {
            "email": user_in.email.lower(),
            "full_name": user_in.full_name,
            "hashed_password": hashed_password,
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        # Remove hashed_password from returned dictionary for safety
        if "hashed_password" in user_dict:
            del user_dict["hashed_password"]
        return user_dict

    async def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify user credentials and return the user document if valid."""
        user = await self.collection.find_one({"email": email.lower()})
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        user["_id"] = str(user["_id"])
        return user

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user document from MongoDB by ObjectId."""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
                return user
        except Exception:
            pass
        return None

    async def add_github_connection(self, user_id: str, connection: Dict[str, Any]) -> bool:
        """Add a GitHub connection to a user, ensuring uniqueness by github_id."""
        try:
            # Check if this specific github_id is already connected to this user
            user = await self.collection.find_one({
                "_id": ObjectId(user_id),
                "github_connections.github_id": connection["github_id"]
            })
            
            if user:
                # Update the existing connection instead
                result = await self.collection.update_one(
                    {"_id": ObjectId(user_id), "github_connections.github_id": connection["github_id"]},
                    {"$set": {"github_connections.$": connection}}
                )
                return result.modified_count > 0
            else:
                # Add a new connection
                result = await self.collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$push": {"github_connections": connection}}
                )
                return result.modified_count > 0
        except Exception:
            return False

    async def remove_github_connection(self, user_id: str, username: str) -> bool:
        """Remove a GitHub connection by username."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"github_connections": {"username": username}}}
            )
            return result.modified_count > 0
        except Exception:
            return False
