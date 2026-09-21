from fastapi import APIRouter, HTTPException, status
from ..models.assessment_models import (
    AssessmentGenerateRequest,
    AssessmentGenerateResponse,
    AssessmentEvaluateRequest,
    AssessmentEvaluateResponse,
)
from ..services.assessment_service import AssessmentService

router = APIRouter(prefix="/api/assessment", tags=["assessment"])
assessment_service = AssessmentService()

@router.post("/generate", response_model=AssessmentGenerateResponse)
async def generate_assessment(req: AssessmentGenerateRequest):
    """
    Generates structured AI assessment questions based on subject, topic, and difficulty mode.
    """
    try:
        return await assessment_service.generate_assessment(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Assessment generation failed", "retryable": True}
        )

@router.post("/evaluate", response_model=AssessmentEvaluateResponse)
async def evaluate_assessment(req: AssessmentEvaluateRequest):
    """
    Evaluates student answers, score, strong topics, weak topics, and AI recommendation.
    """
    try:
        return assessment_service.evaluate_assessment(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Assessment evaluation failed", "retryable": False}
        )
