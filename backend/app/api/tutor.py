from fastapi import APIRouter, HTTPException, status
from ..models.tutor_models import (
    TutorChatRequest,
    TutorChatResponse,
    QuizCheckRequest,
    QuizCheckResponse
)
from ..services.tutor_service import TutorService

router = APIRouter(prefix="/api/tutor", tags=["tutor"])
tutor_service = TutorService()

@router.post("/chat", response_model=TutorChatResponse)
async def tutor_chat(req: TutorChatRequest):
    """
    Main AI Tutor endpoint.
    Processes student query, mode selection, follow-up, or special actions (quiz_me, practice_topic).
    """
    try:
        response = await tutor_service.process_chat(req)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "AI service temporarily unavailable", "retryable": True}
        )

@router.post("/quiz/check", response_model=QuizCheckResponse)
async def check_quiz(req: QuizCheckRequest):
    """
    Evaluates student selected answer for Quiz Me or Practice questions.
    """
    try:
        return tutor_service.check_quiz_answer(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Could not evaluate quiz answer", "retryable": False}
        )

@router.post("/reset")
async def reset_chat(conversation_id: str = "default_conv"):
    """
    Resets the multi-turn conversation context.
    """
    tutor_service.reset_conversation(conversation_id)
    return {"status": "reset", "conversation_id": conversation_id}
