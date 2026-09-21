from pydantic import BaseModel, Field, model_validator
from typing import Any, List, Optional

class StudentContextModel(BaseModel):
    student_name: str = "Santhosh"
    degree: str = "B.Tech CSE"
    current_subject: str = "Computer Networks"
    current_topic: str = "TCP"
    weak_topic: Optional[str] = "TCP connection termination"

class QuizOptionModel(BaseModel):
    key: str # A, B, C, D
    text: str

class QuizModel(BaseModel):
    id: str
    question: str
    options: List[QuizOptionModel]
    correct_key: str
    explanation: str

class TutorChatRequest(BaseModel):
    message: str = Field(..., description="Student message or prompt")
    explanation_mode: str = Field("simple", description="simple | real-world | technical")
    action: Optional[str] = Field(None, description="normal | quiz_me | practice_topic | summarize")
    conversation_id: str = Field("default_conv", description="Unique conversation session identifier")
    student_context: Optional[StudentContextModel] = None

    @model_validator(mode='before')
    @classmethod
    def accept_question_or_message(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'message' not in data and 'question' in data:
                data['message'] = data['question']
            if 'explanation_mode' not in data and 'mode' in data:
                data['explanation_mode'] = data['mode']
        return data

class TutorChatResponse(BaseModel):
    answer: str
    explanation_mode: str
    topic: str
    subject: str
    conversation_id: str
    suggested_followups: List[str] = []
    quiz: Optional[QuizModel] = None
    provider_used: str = "fallback"

class QuizCheckRequest(BaseModel):
    quiz_id: str
    selected_key: str
    correct_key: str
    explanation: str

class QuizCheckResponse(BaseModel):
    is_correct: bool
    title: str
    feedback: str
    explanation: str
