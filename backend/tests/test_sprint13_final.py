import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sprint13_end_to_end_demo_trajectory():
    # 1. Ask Tutor question
    tutor_resp = client.post("/api/tutor/chat", json={
        "message": "Why does TCP use a three-way handshake?",
        "mode": "simple"
    })
    assert tutor_resp.status_code == 200
    tutor_data = tutor_resp.json()
    assert "answer" in tutor_data

    # 2. Vision OCR Analysis
    vis_resp = client.post("/api/vision/analyze", json={
        "image_base64": "mock_base64_math_problem",
        "subject_hint": "Mathematics"
    })
    assert vis_resp.status_code == 200
    assert vis_resp.json()["success"] is True

    # 3. Generate Assessment
    assess_resp = client.post("/api/assessment/generate", json={
        "subject": "Operating Systems",
        "topic": "Process Scheduling",
        "question_count": 5
    })
    assert assess_resp.status_code == 200
    assess_data = assess_resp.json()
    assert len(assess_data["questions"]) > 0


    # 4. Evaluate Assessment & Trigger Weak Topic
    eval_resp = client.post("/api/assessment/evaluate", json={
        "assessment_id": "ass_os_demo",
        "subject": "Operating Systems",
        "topic": "Process Scheduling",
        "difficulty": "medium",
        "submissions": [
            {
                "question_id": "q1",
                "question_text": "Which algorithm causes starvation?",
                "selected_key": "A",
                "correct_key": "B",
                "topic": "Operating Systems",
                "subtopic": "Process Scheduling",
                "explanation": "SJF causes starvation."
            },
            {
                "question_id": "q2",
                "question_text": "What is Round Robin?",
                "selected_key": "C",
                "correct_key": "B",
                "topic": "Operating Systems",
                "subtopic": "Process Scheduling",
                "explanation": "Preemptive time slice."
            }
        ]
    })
    assert eval_resp.status_code == 200

    eval_data = eval_resp.json()
    assert "needs_practice" in eval_data


    # 5. Check Teacher Dashboard receives activity
    dash_resp = client.get("/api/teacher/dashboard")
    assert dash_resp.status_code == 200
    assert dash_resp.json()["total_students"] == 42

    # 6. Teacher Creates Targeted Revision Activity
    act_resp = client.post("/api/teacher/activities", json={
        "topic": "Process Scheduling",
        "subject": "Operating Systems",
        "activity_type": "REVISION_QUIZ",
        "target_student_ids": ["student_001"],
        "question_count": 5,
        "difficulty": "medium"
    })
    assert act_resp.status_code == 200

    # 7. Student Fetches and Acknowledges Pending Action
    pending_resp = client.get("/api/collaboration/actions/student/student_001")
    assert pending_resp.status_code == 200
    actions = pending_resp.json()
    assert len(actions) >= 1

    ack_resp = client.post(f"/api/collaboration/actions/ack/{actions[0]['action_id']}")
    assert ack_resp.status_code == 200

    # 8. Reset Demo State
    reset_resp = client.post("/api/teacher/demo/reset")
    assert reset_resp.status_code == 200
    assert reset_resp.json()["status"] == "success"

def test_sprint13_zero_secret_leakage_audit():
    endpoints = [
        "/api/ai/status",
        "/api/teacher/dashboard",
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
