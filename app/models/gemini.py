from pydantic import BaseModel, Field
from typing import List, Optional

class GeminiPromptRequest(BaseModel):
    prompt: str = Field(..., description="Prompt or instructions for the Gemini model")
    content: Optional[str] = Field(None, description="Optional code or text content to analyze along with the prompt")

class GeminiResponse(BaseModel):
    response_text: str = Field(..., description="The raw generated response from Gemini")
    model_name: str = Field(..., description="The name of the Gemini model used")

class CodeIssue(BaseModel):
    file_path: str = Field(..., description="Path of the file containing the issue")
    line_number: Optional[int] = Field(None, description="Approximate line number")
    severity: str = Field(..., description="Severity level: Info, Warning, Critical")
    description: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested fix or improvement")

class GeminiCodeReview(BaseModel):
    summary: str = Field(..., description="High level summary of the code review findings")
    overall_score: int = Field(..., description="Overall code quality rating from 1 to 10")
    issues: List[CodeIssue] = Field(default_factory=list, description="List of detected code issues")
    refactored_code: Optional[str] = Field(None, description="Refactored or optimized version of the input code (if single file)")
