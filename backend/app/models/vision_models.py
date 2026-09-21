from typing import Optional
from pydantic import BaseModel, Field
from .tutor_models import StudentContextModel

class VisionAnalyzeRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string")
    student_context: Optional[StudentContextModel] = None

class ExtractedQuestionModel(BaseModel):
    detected: bool = True
    question: str
    topic: str = "Computer Science"
    subtopic: Optional[str] = None
    content_type: str = Field("question", description="question | equation | diagram | text | mixed")
    confidence: float = 0.95
    raw_ocr_text: Optional[str] = None
    ai_solution: Optional[str] = None
    explanation: Optional[str] = None

class VisionAnalyzeResponse(BaseModel):
    success: bool = True
    extracted: ExtractedQuestionModel
    provider_used: str = "fallback_vision"
    fallback_used: bool = False
    message: Optional[str] = "Question successfully extracted and solved"
