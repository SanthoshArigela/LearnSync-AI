from typing import List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from ..models.collaboration_models import (
    ClassroomEventModel,
    TeacherActionRequest,
    TeacherActionModel,
    ClassroomSessionModel,
)
from ..services.collaboration_service import CollaborationService

router = APIRouter(prefix="/api/collaboration", tags=["collaboration"])
collab_service = CollaborationService()

@router.websocket("/ws/{client_type}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_type: str, client_id: str):
    """
    WebSocket endpoint for real-time classroom collaboration.
    client_type: 'student' or 'teacher'
    client_id: e.g., 'student_001' or 'teacher_001'
    """
    await collab_service.connect(websocket, client_type, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            if isinstance(data, dict):
                event = ClassroomEventModel(**data)
                await collab_service.publish_event(event)
    except WebSocketDisconnect:
        collab_service.disconnect(websocket, client_type, client_id)
    except Exception:
        collab_service.disconnect(websocket, client_type, client_id)

@router.get("/events", response_model=List[ClassroomEventModel])
async def get_recent_events(limit: int = 20):
    """
    REST fallback endpoint returning recent classroom events for the teacher dashboard feed.
    """
    try:
        return collab_service.get_recent_events(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch classroom events", "details": str(e)}
        )

@router.post("/events", response_model=ClassroomEventModel)
async def post_classroom_event(event: ClassroomEventModel):
    """
    REST fallback endpoint for student mobile apps to post learning events.
    """
    try:
        return await collab_service.publish_event(event)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to publish classroom event", "details": str(e)}
        )

@router.post("/actions", response_model=TeacherActionModel)
async def dispatch_teacher_action(req: TeacherActionRequest):
    """
    Dispatches a teacher targeted revision action to student client(s).
    """
    try:
        return await collab_service.dispatch_teacher_action(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to dispatch teacher action", "details": str(e)}
        )

@router.get("/actions/student/{student_id}", response_model=List[TeacherActionModel])
async def get_student_pending_actions(student_id: str):
    """
    REST fallback polling endpoint for student mobile apps to fetch pending teacher actions.
    """
    try:
        return collab_service.get_pending_actions_for_student(student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to fetch actions for {student_id}", "details": str(e)}
        )

@router.post("/actions/ack/{action_id}")
async def acknowledge_action(action_id: str, student_id: str = "student_001"):
    """
    Acknowledges receipt/launch of a teacher action on the student mobile app.
    """
    try:
        return collab_service.acknowledge_action(action_id, student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to acknowledge action {action_id}", "details": str(e)}
        )

@router.get("/session", response_model=ClassroomSessionModel)
async def get_classroom_session():
    """
    Returns live classroom session status and sync metrics.
    """
    try:
        return collab_service.get_session_status()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch classroom session", "details": str(e)}
        )

@router.get("/health")
async def collaboration_health():
    return {
        "status": "healthy",
        "service": "LearnSync AI Classroom Collaboration Layer"
    }
