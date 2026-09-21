from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models.tutor_models import StudentContextModel

class AIProvider(ABC):
    """
    Abstract AI Provider Interface for LearnSync AI Engine.
    Decouples UI/Service logic from Cloud AI (Gemini), Local On-Device NPU LLMs, or Offline Fallback Engine.
    """

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        explanation_mode: str,
        student_context: Optional[StudentContextModel] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates an educational tutoring response.
        Returns dict containing: 'answer', 'suggested_followups', 'topic', 'subject', 'quiz' (optional).
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    def supports_chat(self) -> bool:
        return True

    @property
    def supports_vision(self) -> bool:
        return False

    @property
    def supports_assessment(self) -> bool:
        return False

    @property
    def supports_offline(self) -> bool:
        return False

    @property
    def is_available(self) -> bool:
        return True

    @property
    def model_name(self) -> str:
        return self.provider_name
