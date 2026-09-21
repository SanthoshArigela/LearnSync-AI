from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StudentClassSummaryModel(BaseModel):
    student_id: str
    name: str
    overall_mastery: int = Field(..., ge=0, le=100)
    weak_topic: str
    trend: str = Field("stable", description="improving | stable | declining")
    recommended_action: str

class ClassTopicInsightModel(BaseModel):
    id: str
    topic: str
    subject: str
    class_mastery: int = Field(..., ge=0, le=100)
    affected_students_count: int
    severity: str = Field("HIGH", description="HIGH | MEDIUM | LOW")
    recommended_teaching_action: str
    trend: str = "declining"

class ClassMisconceptionModel(BaseModel):
    id: str
    topic: str
    subject: str
    misconception_text: str
    affected_students_count: int
    recommended_resource: str

class TeacherRecommendationModel(BaseModel):
    id: str
    priority: str = Field("HIGH", description="HIGH | MEDIUM | LOW")
    topic: str
    subject: str
    affected_students_count: int
    why_evidence: str
    recommended_action: str
    expected_goal: str

class TeachingActivityCreateRequest(BaseModel):
    topic: str
    subject: str = "Computer Science"
    activity_type: str = Field("revision_practice", description="revision_practice | quiz | homework")
    target_student_ids: List[str] = []
    question_count: int = 5
    difficulty: str = "adaptive"

class TeachingActivityModel(BaseModel):
    id: str
    topic: str
    subject: str
    activity_type: str
    target_student_ids: List[str]
    question_count: int
    difficulty: str
    status: str = "created"
    created_at: str

class AssessmentAnalyticsModel(BaseModel):
    id: str
    title: str
    subject: str
    topic: str
    total_students: int = 42
    average_score: int
    completion_rate: int
    most_difficult_question: str
    most_difficult_concept: str

class StudentDetailModel(BaseModel):
    student_id: str
    name: str
    course: str = "B.Tech CSE"
    overall_mastery: int
    recent_assessment_score: int
    trend: str
    subject_masteries: Dict[str, int]
    weak_topics: List[str]
    recent_activities: List[Dict[str, Any]]
    recommended_action: str

class TeacherDashboardModel(BaseModel):
    class_name: str = "B.Tech CSE — AI & ML"
    section: str = "Section A"
    total_students: int = 42
    average_score: int = 78
    students_needing_attention_count: int = 8
    improving_students_count: int = 24
    subject_performances: Dict[str, int]
    classroom_gaps: List[ClassTopicInsightModel]
    misconceptions: List[ClassMisconceptionModel]
    students_needing_attention: List[StudentClassSummaryModel]
    recommendations: List[TeacherRecommendationModel]
    recent_activities: List[TeachingActivityModel] = []
