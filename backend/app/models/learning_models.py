from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TopicMasteryModel(BaseModel):
    subject: str
    topic: str
    subtopic: Optional[str] = None
    mastery_score: int = Field(0, ge=0, le=100)
    attempts: int = 0
    correct: int = 0
    incorrect: int = 0
    trend: str = Field("stable", description="improving | stable | declining")
    status: str = Field("needs_practice", description="strong | moderate | needs_practice")
    last_practiced_at: Optional[str] = None

class SubjectMasteryModel(BaseModel):
    subject: str
    overall_mastery: int = Field(0, ge=0, le=100)
    topics: List[TopicMasteryModel] = []

class RecommendationModel(BaseModel):
    id: str
    title: str
    subject: str
    topic: str
    subtopic: Optional[str] = None
    reason: str
    priority: str = Field("medium", description="high | medium | low")
    action: str = Field("revision", description="revision | practice | tutor | assessment")
    estimated_time_minutes: int = 10
    difficulty: str = Field("medium", description="easy | medium | hard")

class LearningProfileModel(BaseModel):
    student_id: str = "student_001"
    overall_mastery: int = 78
    strong_topics: List[str] = []
    moderate_topics: List[str] = []
    weak_topics: List[str] = []
    subjects: Dict[str, SubjectMasteryModel] = {}
    trends: List[Dict[str, Any]] = []
    recommendations: List[RecommendationModel] = []
    next_best_action: Optional[RecommendationModel] = None

class LearningAnalyzeRequest(BaseModel):
    student_id: str = "student_001"
    assessment_history: List[Dict[str, Any]] = []

class LearningAnalyzeResponse(BaseModel):
    student_id: str
    profile: LearningProfileModel
    message: str = "Learning profile successfully calculated."
