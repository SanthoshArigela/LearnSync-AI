import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_end_to_end_demo_reset():
    response = client.post("/api/teacher/demo/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "reset" in data["message"].lower()

    # Check dashboard baseline state after reset
    dash_resp = client.get("/api/teacher/dashboard")
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["total_students"] == 42
    assert dash_data["average_score"] == 78

def test_collaboration_event_and_action_flow():
    # 1. Post student assessment event
    event_payload = {
        "event_type": "ASSESSMENT_COMPLETED",
        "student_id": "student_001",
        "student_name": "Santhosh K.",
        "topic": "Process Scheduling",
        "subject": "Operating Systems",
        "score": 58,
        "is_weak_topic": True,
        "misconception": "Confusing waiting time with turnaround time"
    }
    event_resp = client.post("/api/collaboration/events", json=event_payload)
    assert event_resp.status_code == 200
    assert event_resp.json()["status"] in ["active", "logged", "success"]

    # 2. Teacher dispatches revision activity
    act_payload = {
        "topic": "Process Scheduling",
        "subject": "Operating Systems",
        "activity_type": "REVISION_QUIZ",
        "target_student_ids": ["student_001"],
        "question_count": 5,
        "difficulty": "medium"
    }
    act_resp = client.post("/api/teacher/activities", json=act_payload)
    assert act_resp.status_code == 200
    act_data = act_resp.json()
    assert act_data["topic"] == "Process Scheduling"

    # 3. Student fetches pending actions
    pending_resp = client.get("/api/collaboration/actions/student/student_001")
    assert pending_resp.status_code == 200
    actions = pending_resp.json()
    assert len(actions) >= 1
    action_id = actions[0]["action_id"]

    # 4. Student acknowledges action
    ack_resp = client.post(f"/api/collaboration/actions/ack/{action_id}")
    assert ack_resp.status_code == 200
    assert ack_resp.json()["status"] in ["acknowledged", "delivered", "success"]

def test_ai_fallback_resilience():
    # Force fallback mode
    status_resp = client.get("/api/ai/status?mode=fallback")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["active_provider"] in ["fallback", "deterministic"]

    # Generate tutor response under fallback
    tutor_resp = client.post(
        "/api/tutor/chat",
        json={"message": "Why does TCP use a three-way handshake?", "mode": "simple"}
    )
    assert tutor_resp.status_code == 200
    tutor_data = tutor_resp.json()
    assert "answer" in tutor_data
    assert len(tutor_data["suggested_followups"]) > 0

def test_vision_fallback_resilience():
    vision_resp = client.post(
        "/api/vision/analyze",
        json={"image_base64": "mock_base64_data", "subject_hint": "Mathematics"}
    )
    assert vision_resp.status_code == 200
    vision_data = vision_resp.json()
    assert vision_data["success"] is True
    assert "extracted" in vision_data
    assert "question" in vision_data["extracted"]

def test_learning_profile_mastery_calculation():
    # Fetch initial learning profile
    prof_resp = client.get("/api/learning/profile")
    assert prof_resp.status_code == 200
    prof_data = prof_resp.json()
    assert "overall_mastery" in prof_data
    assert "weak_topics" in prof_data

def test_zero_secret_leakage_across_all_apis():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
        "/api/collaboration/session",
        "/api/learning/profile",
        "/api/teacher/students"
    ]
    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200
        payload_str = str(resp.json()).lower()
        assert "api_key" not in payload_str
        assert "gemini_api_key" not in payload_str
        assert "secret_key" not in payload_str
