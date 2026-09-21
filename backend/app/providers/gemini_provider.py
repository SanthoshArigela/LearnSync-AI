import json
import time
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from .ai_provider import AIProvider
from .fallback_provider import FallbackProvider
from ..core.config import settings
from ..models.tutor_models import StudentContextModel

logger = logging.getLogger("learnsync.gemini")

class GeminiProvider(AIProvider):
    """
    Google Gemini Cloud AI Provider for LearnSync AI.
    Uses official Google GenAI SDK (google-genai) to deliver personalized,
    mode-adaptive educational tutoring and multi-turn context support.
    """

    def __init__(self):
        self._fallback = FallbackProvider()

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def supports_chat(self) -> bool:
        return True

    @property
    def supports_vision(self) -> bool:
        return True

    @property
    def supports_assessment(self) -> bool:
        return True

    @property
    def supports_offline(self) -> bool:
        return False

    @property
    def is_available(self) -> bool:
        api_key = settings.GEMINI_API_KEY
        return bool(api_key and api_key.strip() and api_key != "your_gemini_api_key_here")

    @property
    def model_name(self) -> str:
        return settings.GEMINI_MODEL or "gemini-3.5-flash-lite"

    def _get_system_instruction(self, explanation_mode: str, action: Optional[str] = None) -> str:
        mode_str = (explanation_mode or "simple").lower()
        if mode_str == "real-world":
            mode_guidance = (
                "EXPLANATION MODE: REAL-WORLD ANALOGY & PRACTICAL APPLICATIONS.\n"
                "- Focus on intuitive everyday analogies, real-life systems, and hardware/software practical scenarios.\n"
                "- Connect abstract concepts to tangible objects or processes students already understand."
            )
        elif mode_str == "technical":
            mode_guidance = (
                "EXPLANATION MODE: DEEP TECHNICAL SPECIFICATIONS & IMPLEMENTATION.\n"
                "- Use precise computer science terminology, RFC/protocol specs, memory layouts, algorithms, and code examples.\n"
                "- Include time/space complexity ($O(n)$, $O(\\log n)$) and underlying systems architecture."
            )
        else:
            mode_guidance = (
                "EXPLANATION MODE: SIMPLE & BEGINNER FRIENDLY.\n"
                "- Keep explanations clear, step-by-step, and accessible.\n"
                "- Use short sentences, intuition first, and minimal unnecessary jargon."
            )

        quiz_guidance = ""
        if action in ["quiz_me", "practice_topic"]:
            quiz_guidance = (
                "\nACTION MANDATE: Include a 'quiz' object in your output JSON with keys:\n"
                "- 'id': string ('quiz_gen_1')\n"
                "- 'question': string (a multiple choice question testing this concept)\n"
                "- 'options': list of 4 objects with 'key' ('A','B','C','D') and 'text'\n"
                "- 'correct_key': string ('A', 'B', 'C', or 'D')\n"
                "- 'explanation': string\n"
            )

        return (
            "You are LearnSync AI — a personalized educational tutor for computer science and engineering students.\n\n"
            "CORE EDUCATIONAL PRINCIPLES:\n"
            "1. Teach rather than merely provide answers. Build conceptual mastery.\n"
            "2. Adapt explanation depth strictly to the student's level and requested mode.\n"
            "3. When appropriate:\n"
            "   - Explain the core concept\n"
            "   - Provide an intuitive explanation and real-world analogy\n"
            "   - Provide code examples when relevant\n"
            "   - Highlight common mistakes to avoid\n"
            "   - Suggest a follow-up practice problem or check question\n"
            "4. Never fabricate facts. If a question is ambiguous, ask for clarification.\n"
            "5. For programming queries (e.g. C, Python, Java, Data Structures), explain the logic, show clean code, and discuss line-by-line mechanics.\n"
            "6. For computer science topics (DBMS, Computer Networks, OS), use accurate terminology without overwhelming beginners.\n\n"
            f"{mode_guidance}\n{quiz_guidance}\n"
            "OUTPUT FORMAT MANDATE:\n"
            "Return a JSON object containing EXACTLY these keys:\n"
            "- 'answer': string (structured Markdown with headings like ### Concept Summary, ### Simple Explanation, ### Real-World Example, ### Key Takeaway)\n"
            "- 'topic': string (e.g. Fundamentals, Inheritance, Pointers, Binary Search Tree, TCP, Normalization, Process, Dictionaries)\n"
            "- 'subject': string (MUST match one of: 'C Programming', 'Java Programming', 'Python Programming', 'Data Structures', 'Computer Networks', 'DBMS', 'Operating Systems', 'Machine Learning')\n"
            "- 'suggested_followups': list of 3 relevant, engaging student follow-up question strings\n"
            "- 'quiz': object or null\n"
        )

    def _build_alternating_contents(self, recent_messages: List[Dict[str, str]]) -> List[types.Content]:
        """
        Ensures strict alternating roles ('user' -> 'model' -> 'user' -> 'model')
        as required by Google GenAI API for multi-turn conversations.
        """
        if not recent_messages:
            return [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text="Explain C programming fundamentals.")]
                )
            ]

        formatted_contents: List[types.Content] = []
        for msg in recent_messages:
            role = "user" if msg.get("role") in ["user", "student"] else "model"
            content_text = msg.get("content", "").strip()
            if not content_text:
                continue

            if formatted_contents and formatted_contents[-1].role == role:
                # Merge consecutive messages from same role to satisfy GenAI multi-turn schema
                prev_text = formatted_contents[-1].parts[0].text
                formatted_contents[-1] = types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=f"{prev_text}\n\n{content_text}")]
                )
            else:
                formatted_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=content_text)]
                    )
                )

        # Gemini multi-turn requests MUST start with a 'user' message
        while formatted_contents and formatted_contents[0].role != "user":
            formatted_contents.pop(0)

        if not formatted_contents:
            formatted_contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text="Explain C programming fundamentals.")]
                )
            ]

        return formatted_contents

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        explanation_mode: str,
        student_context: Optional[StudentContextModel] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        t0 = time.time()
        api_key = settings.GEMINI_API_KEY

        if not self.is_available:
            logger.info("provider=GeminiProvider status=unavailable action=fallback_provider_delegation")
            res_fb = await self._fallback.generate_response(messages, explanation_mode, student_context, action)
            res_fb["fallback_used"] = True
            return res_fb

        client = genai.Client(api_key=api_key)
        system_instruction = self._get_system_instruction(explanation_mode, action)

        # Bounded context window: last 10 messages
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        formatted_contents = self._build_alternating_contents(recent_messages)

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
            response_mime_type="application/json"
        )

        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=formatted_contents,
                    config=config
                )

                latency_ms = int((time.time() - t0) * 1000)
                raw_text = response.text if response else ""

                if raw_text:
                    logger.info(
                        "provider=GeminiProvider model=%s status=success latency_ms=%d fallback_used=false attempt=%d",
                        self.model_name,
                        latency_ms,
                        attempt
                    )
                    parsed = self._parse_gemini_response(raw_text, explanation_mode)
                    if action in ["quiz_me", "practice_topic"] and not parsed.get("quiz"):
                        last_query = messages[-1].get("content", "") if messages else "Computer Science"
                        fb_quiz = self._fallback._build_quiz_response(last_query)
                        parsed["quiz"] = fb_quiz.get("quiz")
                    parsed["fallback_used"] = False
                    parsed["latency_ms"] = latency_ms
                    return parsed

                if attempt < max_attempts:
                    time.sleep(1.0)
                    continue

                logger.warning(
                    "provider=GeminiProvider model=%s status=empty_response latency_ms=%d action=fallback",
                    self.model_name,
                    latency_ms
                )
                res_fb = await self._fallback.generate_response(messages, explanation_mode, student_context, action)
                res_fb["fallback_used"] = True
                return res_fb

            except Exception as e:
                latency_ms = int((time.time() - t0) * 1000)
                if attempt < max_attempts:
                    logger.warning(
                        "provider=GeminiProvider model=%s status=retry_attempt error_type=%s error_msg=%s latency_ms=%d",
                        self.model_name,
                        type(e).__name__,
                        str(e)[:150],
                        latency_ms
                    )
                    time.sleep(1.2)
                    continue

                logger.error(
                    "provider=GeminiProvider model=%s status=error error_type=%s error_msg=%s latency_ms=%d action=fallback",
                    self.model_name,
                    type(e).__name__,
                    str(e)[:150],
                    latency_ms
                )
                res_fb = await self._fallback.generate_response(messages, explanation_mode, student_context, action)
                res_fb["fallback_used"] = True
                return res_fb

    def _parse_gemini_response(self, raw_text: str, mode: str) -> Dict[str, Any]:
        try:
            data = json.loads(raw_text)
            return {
                "answer": data.get("answer", raw_text),
                "explanation_mode": mode,
                "topic": data.get("topic", "Computer Science Topic"),
                "subject": data.get("subject", "Computer Science"),
                "suggested_followups": data.get("suggested_followups", [
                    "Explain this in simpler terms",
                    "Give me a real-world example",
                    "Quiz me on this topic"
                ]),
                "quiz": data.get("quiz"),
                "provider_used": "gemini"
            }
        except Exception:
            return {
                "answer": raw_text,
                "explanation_mode": mode,
                "topic": "Computer Science Topic",
                "subject": "Computer Science",
                "suggested_followups": [
                    "Explain this simply",
                    "Give me a real-world example",
                    "Quiz me on this topic"
                ],
                "quiz": None,
                "provider_used": "gemini"
            }
