import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from .assessment_provider import AssessmentProvider
from .fallback_assessment_provider import FallbackAssessmentProvider
from ..core.config import settings
from ..models.tutor_models import StudentContextModel

logger = logging.getLogger("learnsync.assessment.gemini")

class GeminiAssessmentProvider(AssessmentProvider):
    """
    Google Gemini Assessment Provider for LearnSync AI.
    Generates structured MCQ assessment questions using google-genai SDK.
    """

    def __init__(self):
        self._fallback = FallbackAssessmentProvider()

    @property
    def provider_name(self) -> str:
        return "gemini_assessment"

    async def generate_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
            logger.info("GEMINI_API_KEY not configured. Using FallbackAssessmentProvider.")
            return await self._fallback.generate_questions(subject, topic, difficulty, question_count, student_context)

        try:
            client = genai.Client(api_key=api_key)
            model_name = settings.GEMINI_MODEL or "gemini-3.5-flash-lite"

            system_instruction = (
                f"You are LearnSync AI Assessment Generator for university computer science students.\n"
                f"Generate {question_count} high-quality Multiple Choice Questions (MCQ) for:\n"
                f"Subject: {subject}\nTopic: {topic}\nRequested Difficulty: {difficulty.upper()}\n\n"
                f"Requirements:\n"
                f"1. Each question MUST have exactly 4 options (A, B, C, D) with 1 clear correct answer.\n"
                f"2. Return output STRICTLY as a JSON object matching schema:\n"
                f"{{\n"
                f"  'assessment_id': 'ass_gen_1',\n"
                f"  'subject': '{subject}',\n"
                f"  'topic': '{topic}',\n"
                f"  'requested_difficulty': '{difficulty}',\n"
                f"  'questions': [\n"
                f"    {{\n"
                f"      'id': 'q1',\n"
                f"      'question': 'Question text',\n"
                f"      'topic': '{topic}',\n"
                f"      'subtopic': 'Subtopic name',\n"
                f"      'difficulty': 'easy|medium|hard',\n"
                f"      'options': [\n"
                f"        {{'key': 'A', 'text': 'Option A'}},\n"
                f"        {{'key': 'B', 'text': 'Option B'}},\n"
                f"        {{'key': 'C', 'text': 'Option C'}},\n"
                f"        {{'key': 'D', 'text': 'Option D'}}\n"
                f"      ],\n"
                f"      'correct_key': 'B',\n"
                f"      'explanation': 'Educational explanation why B is correct'\n"
                f"    }}\n"
                f"  ]\n"
                f"}}"
            )

            config = types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )

            response = client.models.generate_content(
                model=model_name,
                contents=system_instruction,
                config=config
            )

            raw_text = response.text if response else ""
            if raw_text:
                parsed = json.loads(raw_text)
                parsed["provider_used"] = self.provider_name
                return parsed

            logger.warning("Gemini Assessment returned empty text. Using FallbackAssessmentProvider.")
            return await self._fallback.generate_questions(subject, topic, difficulty, question_count, student_context)

        except Exception as e:
            logger.error(f"Gemini Assessment error: {type(e).__name__} - {str(e)[:150]}. Using FallbackAssessmentProvider.")
            return await self._fallback.generate_questions(subject, topic, difficulty, question_count, student_context)
