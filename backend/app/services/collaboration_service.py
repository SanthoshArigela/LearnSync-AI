import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from fastapi import WebSocket
from ..models.collaboration_models import (
    ClassroomEventModel,
    TeacherActionRequest,
    TeacherActionModel,
    ClassroomSessionModel,
)

class CollaborationService:
    """
    Singleton service managing real-time WebSocket communication,
    event broadcasting, and REST polling fallback queues between
    Student Web Apps and the Teacher Web Dashboard.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CollaborationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Connected WebSocket clients
        self._student_sockets: Dict[str, List[WebSocket]] = {}
        self._teacher_sockets: List[WebSocket] = []

        # Recent events buffer (capped at 50)
        self._events_buffer: List[ClassroomEventModel] = self._build_demo_initial_events()

        # Pending teacher actions queue per student (student_id -> List[TeacherActionModel])
        self._pending_actions: Dict[str, List[TeacherActionModel]] = {}

        # Classroom Session details
        self._session = ClassroomSessionModel()

    def _build_demo_initial_events(self) -> List[ClassroomEventModel]:
        now_time = datetime.now()
        return [
            ClassroomEventModel(
                event_id="evt_init_001",
                event_type="ASSESSMENT_COMPLETED",
                source="student",
                student_id="student_001",
                student_name="Santhosh K.",
                subject="Operating Systems",
                topic="Process Scheduling",
                subtopic="Round Robin",
                score=58,
                mastery=58,
                severity="HIGH",
                timestamp="Just now",
                payload={"message": "Scored 58% on OS Midterm Quiz 1"}
            ),
            ClassroomEventModel(
                event_id="evt_init_002",
                event_type="WEAK_TOPIC_DETECTED",
                source="student",
                student_id="student_003",
                student_name="Rahul Verma",
                subject="Computer Networks",
                topic="TCP Connection Termination",
                subtopic="4-Way FIN Handshake",
                score=54,
                mastery=54,
                severity="HIGH",
                timestamp="2 mins ago",
                payload={"message": "Repeated misconceptions on FIN-WAIT states"}
            ),
            ClassroomEventModel(
                event_id="evt_init_003",
                event_type="PRACTICE_COMPLETED",
                source="student",
                student_id="student_004",
                student_name="Priya Patel",
                subject="Data Structures",
                topic="Binary Trees",
                subtopic="In-order Traversal",
                score=85,
                mastery=82,
                severity="LOW",
                timestamp="5 mins ago",
                payload={"message": "Completed 5 adaptive practice questions"}
            )
        ]

    async def connect(self, websocket: WebSocket, client_type: str, client_id: str):
        await websocket.accept()
        if client_type == "teacher":
            self._teacher_sockets.append(websocket)
        elif client_type == "student":
            if client_id not in self._student_sockets:
                self._student_sockets[client_id] = []
            self._student_sockets[client_id].append(websocket)

    def disconnect(self, websocket: WebSocket, client_type: str, client_id: str):
        if client_type == "teacher":
            if websocket in self._teacher_sockets:
                self._teacher_sockets.remove(websocket)
        elif client_type == "student":
            if client_id in self._student_sockets and websocket in self._student_sockets[client_id]:
                self._student_sockets[client_id].remove(websocket)

    async def publish_event(self, event: ClassroomEventModel) -> ClassroomEventModel:
        """
        Stores event in buffer and broadcasts to all connected teacher web clients.
        """
        self._events_buffer.insert(0, event)
        if len(self._events_buffer) > 50:
            self._events_buffer = self._events_buffer[:50]

        # Broadcast event to connected teacher sockets
        disconnected_teachers = []
        for ws in self._teacher_sockets:
            try:
                await ws.send_json(event.model_dump())
            except Exception:
                disconnected_teachers.append(ws)

        for ws in disconnected_teachers:
            if ws in self._teacher_sockets:
                self._teacher_sockets.remove(ws)

        return event

    async def dispatch_teacher_action(self, req: TeacherActionRequest) -> TeacherActionModel:
        """
        Dispatches a teacher revision/practice action to student client(s).
        Broadcasts to target student WebSocket and adds to pending actions for REST fallback.
        """
        action = TeacherActionModel(
            action_id=f"act-{uuid.uuid4().hex[:6]}",
            action_type=req.action_type,
            topic=req.topic,
            subject=req.subject,
            target_student_ids=req.target_student_ids,
            question_count=req.question_count,
            difficulty=req.difficulty,
            message=req.message or f"Your teacher sent a {req.topic} revision activity.",
            status="delivered",
            created_at=datetime.now().strftime("%H:%M:%S")
        )

        # Store in pending actions queue for each targeted student
        for student_id in req.target_student_ids:
            if student_id not in self._pending_actions:
                self._pending_actions[student_id] = []
            self._pending_actions[student_id].insert(0, action)

            # Send via WebSocket if student is connected
            if student_id in self._student_sockets:
                disconnected = []
                for ws in self._student_sockets[student_id]:
                    try:
                        await ws.send_json({
                            "type": "TEACHER_ACTION",
                            "action": action.model_dump()
                        })
                    except Exception:
                        disconnected.append(ws)
                for ws in disconnected:
                    self._student_sockets[student_id].remove(ws)

        # Record action in classroom events buffer so teacher dashboard feed sees it
        collab_evt = ClassroomEventModel(
            event_id=f"evt-{uuid.uuid4().hex[:6]}",
            event_type=req.action_type,
            source="teacher",
            student_id=req.target_student_ids[0] if req.target_student_ids else "class",
            student_name="Targeted Students" if len(req.target_student_ids) > 1 else "Santhosh K.",
            subject=req.subject,
            topic=req.topic,
            severity="MEDIUM",
            status="delivered",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            payload={
                "message": f"Sent {req.question_count}-question {req.difficulty} revision for {req.topic}",
                "action_id": action.action_id
            }
        )
        await self.publish_event(collab_evt)
        return action

    def get_recent_events(self, limit: int = 20) -> List[ClassroomEventModel]:
        return self._events_buffer[:limit]

    def get_pending_actions_for_student(self, student_id: str) -> List[TeacherActionModel]:
        return self._pending_actions.get(student_id, [])

    def acknowledge_action(self, action_id: str, student_id: str) -> Dict[str, Any]:
        if student_id in self._pending_actions:
            self._pending_actions[student_id] = [
                a for a in self._pending_actions[student_id] if a.action_id != action_id
            ]
        return {"status": "acknowledged", "action_id": action_id}

    def get_session_status(self) -> ClassroomSessionModel:
        self._session.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self._session
