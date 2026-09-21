from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.tutor_models import StudentContextModel

class AssessmentProvider(ABC):
    """
    Abstract Assessment Provider Interface.
    Decouples quiz question generation from Gemini API, Local models, or Fallback Question Banks.
    """

    @abstractmethod
    async def generate_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        """
        Generates structured assessment questions.
        Returns dict matching AssessmentGenerateResponse schema.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
