"""Service module for interacting with the Google Gemini generative AI API."""

import logging
from typing import Optional

from google import genai
from google.genai import types

from app.config import settings
from app.models.gemini import GeminiResponse, GeminiCodeReview

logger = logging.getLogger(__name__)


class GeminiService:
    """Provides methods to generate text and perform code reviews using Gemini."""

    def __init__(self):
        """Initialize the Gemini service."""
        # The new Google GenAI SDK automatically grabs the GEMINI_API_KEY environment variable.
        # We can also supply it explicitly if configured in our settings object.
        api_key = settings.GEMINI_API_KEY
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
        # Default model for developer / coding tasks
        self.model = settings.GEMINI_MODEL_NAME

    async def generate_text(
        self, prompt: str, content: Optional[str] = None
    ) -> GeminiResponse:
        """Asynchronously generates raw text output from Gemini."""
        combined_content = f"{prompt}\n\nContent:\n{content}" if content else prompt

        try:
            # Using the aio (async io) client within the Google GenAI SDK
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=combined_content
            )
            return GeminiResponse(
                response_text=response.text,
                model_name=self.model
            )
        except Exception as e:
            logger.error("Error calling Gemini API: %s", str(e))
            raise

    async def analyze_code(
        self, code_content: str, file_path: str
    ) -> GeminiCodeReview:
        """Asynchronously reviews code quality and returns structured JSON schema output."""
        prompt = (
            f"Please perform a detailed code review for the following file: '{file_path}'. "
            "Identify syntax errors, code quality issues, "
            "security vulnerabilities, and logic flaws. "
            "Provide severity levels, descriptions, and suggestions. "
            "Finally, evaluate the code structure and provide an "
            "overall score from 1 (poor) to 10 (excellent)."
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=[prompt, code_content],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GeminiCodeReview,
                    temperature=0.2
                )
            )

            # The response.text will be parsed automatically or casted into our Pydantic model
            # types.GenerateContentConfig ensures response structure matches response_schema
            review_json = response.text
            return GeminiCodeReview.model_validate_json(review_json)

        except Exception as e:
            logger.error(
                "Error performing code review with Gemini: %s", str(e)
            )
            raise

    async def analyze_repository_structure(
        self, structure_outline: str
    ) -> GeminiCodeReview:
        """Analyze repository directory structure and provide a structural review."""
        prompt = (
            "Please perform a detailed structural review of the following "
            "repository directory listing. Evaluate the project organization, "
            "identify missing best-practice files (e.g., README, LICENSE, "
            ".gitignore, CI configs, tests), assess the naming conventions, "
            "and suggest improvements. Provide severity levels, descriptions, "
            "and suggestions. Finally, evaluate the overall structure and "
            "provide a score from 1 (poor) to 10 (excellent)."
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=[prompt, structure_outline],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GeminiCodeReview,
                    temperature=0.2
                )
            )
            review_json = response.text
            return GeminiCodeReview.model_validate_json(review_json)

        except Exception as e:
            logger.error(
                "Error performing structure review with Gemini: %s", str(e)
            )
            raise
