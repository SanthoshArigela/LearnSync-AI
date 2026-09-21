from typing import Dict, List, Any
from ..models.tutor_models import (
    TutorChatRequest,
    TutorChatResponse,
    QuizCheckRequest,
    QuizCheckResponse,
    QuizModel
)
from ..providers.ai_provider import AIProvider
from ..providers.gemini_provider import GeminiProvider

class ConversationManager:
    """In-memory multi-turn conversation history repository."""

    def __init__(self):
        self._conversations: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        return self._conversations.get(conversation_id, [])

    def add_message(self, conversation_id: str, role: str, content: str):
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []
        self._conversations[conversation_id].append({"role": role, "content": content})
        # Keep last 10 turns to avoid buffer bloat
        if len(self._conversations[conversation_id]) > 20:
            self._conversations[conversation_id] = self._conversations[conversation_id][-20:]

    def reset_conversation(self, conversation_id: str):
        self._conversations[conversation_id] = []


from .ai_router_service import AIRouterService

class TutorService:
    def __init__(self, provider: AIProvider = None):
        self._custom_provider = provider
        self.router = AIRouterService()
        self.conv_manager = ConversationManager()

    async def process_chat(self, req: TutorChatRequest) -> TutorChatResponse:
        conv_id = req.conversation_id or "default_conv"

        # Record student user message
        self.conv_manager.add_message(conv_id, "user", req.message)
        history = self.conv_manager.get_history(conv_id)

        # Resolve provider via AIRouterService if no custom provider given
        active_provider = self._custom_provider or self.router.resolve_provider()

        # Generate response via active AI Provider abstraction
        res = await active_provider.generate_response(
            messages=history,
            explanation_mode=req.explanation_mode,
            student_context=req.student_context,
            action=req.action
        )

        answer_text = res.get("answer", "")
        # Record AI answer into multi-turn history
        self.conv_manager.add_message(conv_id, "assistant", answer_text)

        quiz_data = res.get("quiz")
        quiz_model = None
        if isinstance(quiz_data, dict):
            try:
                quiz_model = QuizModel(**quiz_data)
            except Exception:
                quiz_model = None

        return TutorChatResponse(
            answer=answer_text,
            explanation_mode=res.get("explanation_mode", req.explanation_mode),
            topic=res.get("topic", "Computer Networks"),
            subject=res.get("subject", "Computer Science"),
            conversation_id=conv_id,
            suggested_followups=res.get("suggested_followups", []),
            quiz=quiz_model,
            provider_used=res.get("provider_used", active_provider.provider_name),
        )

    def check_quiz_answer(self, req: QuizCheckRequest) -> QuizCheckResponse:
        is_correct = req.selected_key.strip().upper() == req.correct_key.strip().upper()

        if is_correct:
            return QuizCheckResponse(
                is_correct=True,
                title="Correct! 🎉",
                feedback=f"Option {req.selected_key} is correct!",
                explanation=req.explanation
            )
        else:
            return QuizCheckResponse(
                is_correct=False,
                title="Not quite 💡",
                feedback=f"Option {req.selected_key} is incorrect. The correct answer is Option {req.correct_key}.",
                explanation=req.explanation
            )

    def reset_conversation(self, conversation_id: str):
        self.conv_manager.reset_conversation(conversation_id)
