from fastapi import APIRouter
from app.api.v1 import github, gemini, analyze, auth

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(github.router, prefix="/github", tags=["GitHub"])
api_router.include_router(gemini.router, prefix="/gemini", tags=["Gemini"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

