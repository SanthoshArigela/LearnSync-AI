from typing import Dict, Any, Optional
from .assessment_provider import AssessmentProvider
from .fallback_assessment_provider import FallbackAssessmentProvider
from ..models.tutor_models import StudentContextModel

class LocalAssessmentProvider(AssessmentProvider):
    """
    Local / On-Device NPU Assessment Provider Architecture Stub.
    Prepared for future local open-source question generation model integration.
    """

    def __init__(self):
        self._fallback = FallbackAssessmentProvider()

    @property
    def provider_name(self) -> str:
        return "local_assessment"

    async def generate_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        res = await self._fallback.generate_questions(subject, topic, difficulty, question_count, student_context)
        res["provider_used"] = "local_assessment"
        return res
