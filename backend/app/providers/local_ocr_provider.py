from typing import Dict, Any, Optional
from .vision_provider import VisionProvider
from .fallback_vision_provider import FallbackVisionProvider
from ..models.tutor_models import StudentContextModel

class LocalOCRProvider(VisionProvider):
    """
    Local OCR / On-Device NPU Vision Provider Architecture Stub.
    Prepared for future Tesseract / Snapdragon NPU local OCR model integration.
    """

    def __init__(self):
        self._fallback = FallbackVisionProvider()

    @property
    def provider_name(self) -> str:
        return "local_ocr"

    async def analyze_image(
        self,
        image_base64: str,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        res = await self._fallback.analyze_image(image_base64, student_context)
        res["provider_used"] = "local_ocr"
        return res
