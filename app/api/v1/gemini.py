"""API routes for direct Gemini AI prompt endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_gemini_service
from app.models.gemini import GeminiPromptRequest, GeminiResponse
from app.services.gemini import GeminiService

router = APIRouter()


@router.post("/prompt", response_model=GeminiResponse)
async def prompt_gemini(
    request: GeminiPromptRequest,
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    """Directly prompt the Gemini model with a user instruction and optional context."""
    try:
        return await gemini_service.generate_text(
            prompt=request.prompt,
            content=request.content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini generation failed: {str(e)}"
        ) from e
