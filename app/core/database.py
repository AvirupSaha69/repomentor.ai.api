"""MongoDB database connection management and lifecycle utilities."""
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

logger = logging.getLogger(__name__)


class Database:  # pylint: disable=too-few-public-methods
    """Holds the MongoDB client and database instance references."""

    client: AsyncIOMotorClient = None
    db = None


db_instance = Database()


async def connect_to_mongo():
    """Create database connection."""
    logger.info("Connecting to MongoDB...")
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db_instance.db = db_instance.client[settings.MONGODB_DB_NAME]
    logger.info("Successfully connected to MongoDB.")


async def close_mongo_connection():
    """Close database connection."""
    if db_instance.client:
        logger.info("Closing MongoDB connection...")
        db_instance.client.close()
        logger.info("MongoDB connection closed.")


def get_database():
    """Dependency provider for database instance."""
    return db_instance.db
