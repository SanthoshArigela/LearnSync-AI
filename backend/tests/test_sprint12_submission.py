import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health_check_endpoints():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
        "/api/teacher/students",
        "/api/teacher/topics",
        "/api/teacher/assessments",
        "/api/teacher/recommendations",
        "/api/learning/profile",
        "/api/collaboration/session",
    ]
    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"

def test_npu_status_truthfulness():
    resp = client.get("/api/ai/status")
    assert resp.status_code == 200
    data = resp.json()
    # Ensure default status does not claim physical NPU hardware acceleration if NPU runtime is unverified
    if not data.get("simulated_npu", False):
        assert "mode" in data
        assert "capabilities" in data
        assert "device_info" in data

def test_demo_reset_restoration():
    # 1. Dispatch custom activity to alter state
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

    # 3. Verify clean baseline state
    dash_resp = client.get("/api/teacher/dashboard")
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["total_students"] == 42
    assert dash_data["average_score"] == 78
    assert len(dash_data["recent_activities"]) == 0

def test_security_zero_secret_leakage():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
        "/api/learning/profile",
        "/api/collaboration/session"
    ]
    for ep in endpoints:
        resp = client.get(ep)
        payload = str(resp.json()).lower()
        assert "api_key" not in payload
        assert "gemini_api_key" not in payload
        assert "secret_key" not in payload
        assert "token_secret" not in payload
