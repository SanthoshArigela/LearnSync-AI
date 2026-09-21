import json
import base64
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from .vision_provider import VisionProvider
from .fallback_vision_provider import FallbackVisionProvider
from ..core.config import settings
from ..models.tutor_models import StudentContextModel

logger = logging.getLogger("learnsync.vision.gemini")

class GeminiVisionProvider(VisionProvider):
    """
    Google Gemini Multimodal Vision AI Provider for LearnSync AI.
    Analyzes image base64 data using google-genai SDK and extracts question text & metadata.
    """

    def __init__(self):
        self._fallback = FallbackVisionProvider()

    @property
    def provider_name(self) -> str:
        return "gemini_vision"

    async def analyze_image(
        self,
        image_base64: str,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
            logger.info("GEMINI_API_KEY not configured. Falling back to FallbackVisionProvider.")
            return await self._fallback.analyze_image(image_base64, student_context)

        try:
            clean_b64 = image_base64
            mime_type = "image/jpeg"
            if "," in clean_b64:
                header, clean_b64 = clean_b64.split(",", 1)
                if "image/png" in header:
                    mime_type = "image/png"
                elif "image/webp" in header:
                    mime_type = "image/webp"

            image_bytes = base64.b64decode(clean_b64)

            client = genai.Client(api_key=api_key)
            model_name = settings.GEMINI_MODEL or "gemini-3.5-flash-lite"

            prompt_text = (
                "You are LearnSync AI Multimodal Vision Assistant.\n"
                "Analyze this image of handwritten notes, study material, textbook, or diagram.\n"
                "1. Extract the exact text or problem written in the image accurately.\n"
                "2. Identify the subject/topic.\n"
                "3. Solve and thoroughly explain the question/request found in the image.\n"
                "   - If the user asks to explain a language or concept (e.g. 'Explain me C-language from the beginning'), provide a complete, structured tutorial starting from fundamentals (variables, main(), loops, functions, pointers).\n"
                "   - If it is a math problem or code snippet, provide a step-by-step solution.\n"
                "Return output STRICTLY as a JSON object with keys:\n"
                "- 'detected': boolean\n"
                "- 'question': string (clean extracted question or request text)\n"
                "- 'topic': string (e.g. C Programming, Computer Networks, DBMS, Data Structures, Operating Systems, Mathematics)\n"
                "- 'subtopic': string\n"
                "- 'content_type': 'question' | 'equation' | 'diagram' | 'text' | 'mixed'\n"
                "- 'confidence': float (between 0.0 and 1.0)\n"
                "- 'raw_ocr_text': string (exact raw OCR text)\n"
                "- 'ai_solution': string (comprehensive step-by-step educational solution and explanation in detailed Markdown format)\n"
                "- 'explanation': string (concise summary of the solution concept)"
            )

            contents = [
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt_text
            ]

            config = types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

            raw_text = response.text if response else ""
            if raw_text:
                parsed = json.loads(raw_text)
                parsed["provider_used"] = self.provider_name
                parsed["fallback_used"] = False
                return parsed

            logger.warning("Gemini Vision API returned empty response. Using FallbackVisionProvider.")
            return await self._fallback.analyze_image(image_base64, student_context)

        except Exception as e:
            logger.error(f"Gemini Vision invocation error: {type(e).__name__} - {str(e)[:150]}. Using FallbackVisionProvider.")
            return await self._fallback.analyze_image(image_base64, student_context)
