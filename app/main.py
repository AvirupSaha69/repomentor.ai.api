from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifecycle startup event
    await connect_to_mongo()
    yield
    # Lifecycle shutdown event
    await close_mongo_connection()

app = FastAPI(
    title="RepoMentor API",
    description="Python API integrating MongoDB, GitHub API, and Gemini API for codebase analysis.",
    version="1.0.0",
    lifespan=lifespan
)

# Root / health endpoint
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "debug_mode": settings.DEBUG
    }

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")
