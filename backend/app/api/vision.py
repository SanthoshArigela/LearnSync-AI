from fastapi import APIRouter, HTTPException, status
from ..models.vision_models import VisionAnalyzeRequest, VisionAnalyzeResponse
from ..services.vision_service import VisionService

router = APIRouter(prefix="/api/vision", tags=["vision"])
vision_service = VisionService()

@router.post("/analyze", response_model=VisionAnalyzeResponse)
async def analyze_image(req: VisionAnalyzeRequest):
    """
    Vision AI endpoint.
    Extracts text, equation, topic, and subtopic metadata from captured student image.
    """
    try:
        return await vision_service.analyze_question_image(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Vision AI processing failed", "retryable": True}
        )
