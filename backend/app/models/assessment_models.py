from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .tutor_models import StudentContextModel, QuizOptionModel

class GeneratedQuestionModel(BaseModel):
    id: str
    question: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: str = Field("medium", description="easy | medium | hard")
    options: List[QuizOptionModel]
    correct_key: str
    explanation: str

class AssessmentGenerateRequest(BaseModel):
    subject: str = "Computer Networks"
    topic: str = "TCP"
    difficulty: str = Field("adaptive", description="easy | medium | hard | adaptive")
    question_count: int = Field(5, ge=1, le=10)
    student_context: Optional[StudentContextModel] = None

class AssessmentGenerateResponse(BaseModel):
    assessment_id: str
    subject: str
    topic: str
    requested_difficulty: str
    questions: List[GeneratedQuestionModel]
    provider_used: str = "fallback_assessment"

class QuestionAnswerSubmission(BaseModel):
    question_id: str
    selected_key: str
    question_text: str
    correct_key: str
    topic: str
    subtopic: Optional[str] = None
    explanation: str

class AssessmentEvaluateRequest(BaseModel):
    assessment_id: str
    subject: str
    topic: str
    difficulty: str
    submissions: List[QuestionAnswerSubmission]
    adaptive_path: Optional[List[str]] = None
    student_context: Optional[StudentContextModel] = None

class AssessmentEvaluateResponse(BaseModel):
    assessment_id: str
    score: int
    total: int
    percentage: int
    strong_areas: List[str]
    needs_practice: List[str]
    ai_recommendation: str
    adaptive_path_summary: Optional[str] = None
    mistakes: List[Dict[str, Any]] = []

class AssessmentHistoryModel(BaseModel):
    id: str
    subject: str
    topic: str
    score: int
    total: int
    percentage: int
    difficulty: str
    timestamp: str
