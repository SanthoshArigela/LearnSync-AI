import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_collaboration_events():
    response = client.get("/api/collaboration/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "event_type" in data[0]

def test_post_classroom_event():
    evt = {
        "event_type": "ASSESSMENT_COMPLETED",
        "source": "student",
        "student_id": "student_001",
        "student_name": "Santhosh K.",
        "subject": "Operating Systems",
        "topic": "Process Scheduling",
        "score": 58,
        "mastery": 58,
        "severity": "HIGH",
        "payload": {"details": "Completed test quiz"}
    }
    response = client.post("/api/collaboration/events", json=evt)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Process Scheduling"
    assert data["event_type"] == "ASSESSMENT_COMPLETED"

def test_dispatch_teacher_action():
    action_req = {
        "action_type": "START_REVISION",
        "topic": "Process Scheduling",
        "subject": "Operating Systems",
        "target_student_ids": ["student_001"],
        "question_count": 5,
        "difficulty": "adaptive",
        "message": "Revise Process Scheduling now"
    }
    response = client.post("/api/collaboration/actions", json=action_req)
    assert response.status_code == 200
    data = response.json()
    assert data["action_type"] == "START_REVISION"
    assert data["topic"] == "Process Scheduling"

def test_get_student_pending_actions():
    response = client.get("/api/collaboration/actions/student/student_001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["topic"] == "Process Scheduling"

def test_acknowledge_action():
    pending_res = client.get("/api/collaboration/actions/student/student_001")
    data = pending_res.json()
    if data:
        action_id = data[0]["action_id"]
        ack_res = client.post(f"/api/collaboration/actions/ack/{action_id}?student_id=student_001")
        assert ack_res.status_code == 200
        assert ack_res.json()["status"] == "acknowledged"

def test_get_classroom_session():
    response = client.get("/api/collaboration/session")
    assert response.status_code == 200
    data = response.json()
    assert data["class_id"] == "class_btech_cse_sec_a"
    assert data["is_live"] is True

def test_collaboration_health():
    response = client.get("/api/collaboration/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
