from fastapi import APIRouter, HTTPException, status
from ..models.vision_models import VisionAnalyzeRequest, VisionAnalyzeResponse
from ..services.vision_service import VisionService

router = APIRouter(prefix="/api/vision", tags=["vision"])
vision_service = VisionService()

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB limit
MAX_B64_LENGTH = int(MAX_IMAGE_SIZE_BYTES * 1.38)  # Base64 overhead buffer

@router.post("/analyze", response_model=VisionAnalyzeResponse)
async def analyze_image(req: VisionAnalyzeRequest):
    """
    Vision AI endpoint.
    Validates image format/size and processes multimodal image analysis in-memory.
    """
    b64_str = req.image_base64 or ""
    if not b64_str.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Image base64 payload cannot be empty", "retryable": False}
        )

    if len(b64_str) > MAX_B64_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Image file exceeds maximum allowed size of 5MB", "retryable": False}
        )

    if "," in b64_str[:100]:
        header = b64_str.split(",", 1)[0].lower()
        valid_mimes = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
        if not any(mime in header for mime in valid_mimes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Unsupported image format. Allowed formats: PNG, JPG, JPEG, WEBP", "retryable": False}
            )

    try:
        return await vision_service.analyze_question_image(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Vision AI processing failed", "retryable": True}
        )
