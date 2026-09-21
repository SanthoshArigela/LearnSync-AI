from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class ClassroomEventModel(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:6]}")
    event_type: str = Field(
        ...,
        description="ASSESSMENT_COMPLETED | WEAK_TOPIC_DETECTED | REPEATED_MISTAKE | PRACTICE_COMPLETED | QUESTION_ASKED | VISION_QUESTION | LEARNING_PROGRESS_UPDATED | START_REVISION | SEND_PRACTICE | ASSIGN_ASSESSMENT | RECOMMEND_TOPIC"
    )
    source: str = Field("student", description="student | teacher")
    student_id: str = "student_001"
    student_name: str = "Santhosh K."
    subject: str = "Operating Systems"
    topic: str = "Process Scheduling"
    subtopic: Optional[str] = "Round Robin & Priority"
    score: Optional[int] = None
    mastery: Optional[int] = None
    severity: str = "HIGH"
    status: str = "active"  # active | delivered | acknowledged
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    payload: Dict[str, Any] = Field(default_factory=dict)

class ClassroomSessionModel(BaseModel):
    class_id: str = "class_btech_cse_sec_a"
    class_name: str = "B.Tech CSE — AI & ML"
    section: str = "Section A"
    teacher_name: str = "Dr. R. Sharma"
    total_students: int = 42
    active_students_count: int = 36
    offline_students_count: int = 6
    is_live: bool = True
    last_sync: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class TeacherActionRequest(BaseModel):
    action_type: str = Field("START_REVISION", description="START_REVISION | SEND_PRACTICE | ASSIGN_ASSESSMENT | RECOMMEND_TOPIC")
    topic: str
    subject: str = "Operating Systems"
    target_student_ids: List[str] = ["student_001"]
    question_count: int = 5
    difficulty: str = "adaptive"
    message: Optional[str] = "Your teacher sent you a targeted revision activity."

class TeacherActionModel(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act-{uuid.uuid4().hex[:6]}")
    action_type: str
    topic: str
    subject: str
    target_student_ids: List[str]
    question_count: int
    difficulty: str
    message: str
    status: str = "delivered"
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
