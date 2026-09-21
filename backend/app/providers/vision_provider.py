from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.tutor_models import StudentContextModel

class VisionProvider(ABC):
    """
    Abstract Vision AI Provider Interface.
    Decouples camera OCR & Multimodal Vision processing from Gemini, local OCR, or Fallback.
    """

    @abstractmethod
    async def analyze_image(
        self,
        image_base64: str,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        """
        Analyzes image and extracts structured question information.
        Returns dict matching ExtractedQuestionModel schema.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
