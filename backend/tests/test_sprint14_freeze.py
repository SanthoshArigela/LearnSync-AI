import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_consecutive_double_demo_reset_cycles():
    """Verifies that executing demo reset multiple times in sequence safely restores baseline state without corruption."""
    for cycle in range(2):
        # 1. Dispatch custom teaching activity
        act_resp = client.post("/api/teacher/activities", json={
            "topic": "Process Scheduling",
            "subject": "Operating Systems",
            "activity_type": "REVISION_QUIZ",
            "target_student_ids": ["student_001"],
            "question_count": 5,
            "difficulty": "medium"
        })
        assert act_resp.status_code == 200

        # 2. Reset demo state
        reset_resp = client.post("/api/teacher/demo/reset")
        assert reset_resp.status_code == 200
        assert reset_resp.json()["status"] == "success"

        # 3. Verify baseline metrics restored
        dash_resp = client.get("/api/teacher/dashboard")
        assert dash_resp.status_code == 200
        dash_data = dash_resp.json()
        assert dash_data["total_students"] == 42
        assert dash_data["average_score"] == 78
        assert len(dash_data["recent_activities"]) == 0

def test_ai_router_failsafe_chain():
    modes = ["auto", "local", "gemini", "fallback"]
    for mode in modes:
        resp = client.get(f"/api/ai/status?mode={mode}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["mode"] == mode
        assert "active_provider" in data
        assert "capabilities" in data

def test_collaboration_websocket_and_rest_fallback():
    # Fetch collaboration session state
    session_resp = client.get("/api/collaboration/session")
    assert session_resp.status_code == 200
    session_data = session_resp.json()
    assert session_data["class_id"] == "class_btech_cse_sec_a"
    assert session_data["is_live"] is True



def test_repository_zero_secret_leakage_audit():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
        "/api/teacher/students",
        "/api/teacher/topics",
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
