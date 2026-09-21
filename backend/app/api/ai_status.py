from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from ..services.ai_router_service import AIRouterService

router = APIRouter(prefix="/api/ai", tags=["ai_status"])
router_service = AIRouterService()

class ModeChangeRequest(BaseModel):
    mode: str = Field(..., description="auto | local | gemini | fallback")
    force_local: Optional[bool] = Field(False, description="Force local provider available")
    simulated_npu: Optional[bool] = Field(False, description="Simulate NPU hardware acceleration")

@router.get("/status")
async def get_ai_status(
    mode: Optional[str] = Query(None, description="Optional provider mode override"),
    force_local: Optional[bool] = Query(False, description="Force local model available for demo"),
    simulated_npu: Optional[bool] = Query(False, description="Simulate hardware NPU acceleration for demo")
):
    """
    Returns AI Provider Routing Status, capability matrix, and active provider info without exposing secrets.
    """
    try:
        if force_local or simulated_npu:
            service = AIRouterService(force_local_available=force_local, simulated_npu=simulated_npu)
            return service.get_ai_status(mode_override=mode)
        return router_service.get_ai_status(mode_override=mode)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch AI status", "details": str(e)}
        )

@router.post("/mode")
async def set_ai_mode(req: ModeChangeRequest):
    """
    Sets temporary AI provider mode override for demonstration purposes.
    """
    try:
        valid_modes = ["auto", "local", "gemini", "fallback"]
        if req.mode.lower() not in valid_modes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": f"Invalid mode. Supported modes: {valid_modes}"}
            )
        service = AIRouterService(
            force_local_available=req.force_local or False,
            simulated_npu=req.simulated_npu or False
        ) if (req.force_local or req.simulated_npu) else router_service

        return service.get_ai_status(mode_override=req.mode.lower())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to update AI mode", "details": str(e)}
        )

