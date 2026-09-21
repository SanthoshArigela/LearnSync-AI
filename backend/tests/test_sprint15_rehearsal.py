import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sprint15_double_demo_reset_rehearsal():
    """Verifies that consecutive demo resets leave the system in pristine baseline state."""
    for cycle in range(1, 3):
        # Dispatch dummy activity
        act_resp = client.post("/api/teacher/activities", json={
            "topic": "Process Scheduling",
            "subject": "Operating Systems",
            "activity_type": "REVISION_QUIZ",
            "target_student_ids": ["student_001"],
            "question_count": 5,
            "difficulty": "medium"
        })
        assert act_resp.status_code == 200

        # Execute demo reset
        reset_resp = client.post("/api/teacher/demo/reset")
        assert reset_resp.status_code == 200
        assert reset_resp.json()["status"] == "success"

        # Verify baseline metrics
        dash_resp = client.get("/api/teacher/dashboard")
        assert dash_resp.status_code == 200
        dash_data = dash_resp.json()
        assert dash_data["total_students"] == 42
        assert dash_data["average_score"] == 78
        assert len(dash_data["recent_activities"]) == 0

def test_sprint15_ai_provider_fallback_matrix():
    modes = ["auto", "local", "gemini", "fallback"]
    for mode in modes:
        resp = client.get(f"/api/ai/status?mode={mode}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["mode"] == mode
        assert "active_provider" in data
        assert "capabilities" in data
        assert "device_info" in data

def test_sprint15_collaboration_rest_polling_fallback():
    # 1. Fetch recent events
    events_resp = client.get("/api/collaboration/events")
    assert events_resp.status_code == 200
    events = events_resp.json()
    assert isinstance(events, list)

    # 2. Fetch pending student actions
    actions_resp = client.get("/api/collaboration/actions/student/student_001")
    assert actions_resp.status_code == 200
    assert isinstance(actions_resp.json(), list)

def test_sprint15_secret_protection_audit():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
        "/api/teacher/students",
        "/api/teacher/topics",
        "/api/teacher/assessments",
        "/api/learning/profile",
        "/api/collaboration/session"
    ]
    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200
        payload = str(resp.json()).lower()
        assert "api_key" not in payload
        assert "gemini_api_key" not in payload
        assert "secret_key" not in payload
        assert "password" not in payload
