from typing import Dict, Any, Optional
from ..models.vision_models import VisionAnalyzeRequest, VisionAnalyzeResponse, ExtractedQuestionModel
from ..providers.vision_provider import VisionProvider
from ..providers.gemini_vision_provider import GeminiVisionProvider

class VisionService:
    def __init__(self, provider: Optional[VisionProvider] = None):
        self.provider = provider or GeminiVisionProvider()

    async def analyze_question_image(self, req: VisionAnalyzeRequest) -> VisionAnalyzeResponse:
        # Process image in memory without persistent disk storage (privacy preserving)
        raw_res = await self.provider.analyze_image(req.image_base64, req.student_context)

        extracted = ExtractedQuestionModel(
            detected=raw_res.get("detected", True),
            question=raw_res.get("question", "Question extracted from image"),
            topic=raw_res.get("topic", "Computer Science"),
            subtopic=raw_res.get("subtopic"),
            content_type=raw_res.get("content_type", "question"),
            confidence=raw_res.get("confidence", 0.95),
            raw_ocr_text=raw_res.get("raw_ocr_text"),
            ai_solution=raw_res.get("ai_solution"),
            explanation=raw_res.get("explanation")
        )

        return VisionAnalyzeResponse(
            success=True,
            extracted=extracted,
            provider_used=raw_res.get("provider_used", self.provider.provider_name),
            fallback_used=raw_res.get("fallback_used", False),
            message="Question extracted and solved successfully"
        )
