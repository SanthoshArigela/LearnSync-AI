from typing import List
from fastapi import APIRouter, HTTPException, status
from ..models.learning_models import (
    LearningProfileModel,
    LearningAnalyzeRequest,
    LearningAnalyzeResponse,
    RecommendationModel,
)
from ..services.learning_profile_service import LearningProfileService

router = APIRouter(prefix="/api/learning", tags=["learning"])
learning_profile_service = LearningProfileService()

@router.get("/profile", response_model=LearningProfileModel)
async def get_learning_profile():
    """
    Returns the student's current learning profile, subject masteries,
    weak/strong areas, and personalized recommendations.
    """
    try:
        return learning_profile_service.get_profile()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch learning profile", "details": str(e)}
        )

@router.post("/analyze", response_model=LearningAnalyzeResponse)
async def analyze_learning_profile(req: LearningAnalyzeRequest):
    """
    Analyzes student assessment history, updates topic mastery,
    detects learning gaps, and returns the updated learning profile.
    """
    try:
        profile = learning_profile_service.get_profile()
        return LearningAnalyzeResponse(
            student_id=req.student_id,
            profile=profile,
            message="Learning profile successfully updated."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to analyze learning profile", "details": str(e)}
        )

@router.get("/recommendations", response_model=List[RecommendationModel])
async def get_recommendations():
    """
    Returns prioritized learning recommendations (High, Medium, Low) for the student.
    """
    try:
        profile = learning_profile_service.get_profile()
        return profile.recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch recommendations", "details": str(e)}
        )
