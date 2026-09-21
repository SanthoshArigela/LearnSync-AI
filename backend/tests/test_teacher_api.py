import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_get_teacher_dashboard():
    response = client.get("/api/teacher/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_students"] == 42
    assert data["average_score"] == 78
    assert "classroom_gaps" in data
    assert "students_needing_attention" in data
    assert "recommendations" in data
    assert len(data["classroom_gaps"]) > 0

def test_api_get_teacher_students():
    response = client.get("/api/teacher/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 8
    assert data[0]["student_id"] == "student_001"

def test_api_get_student_detail():
    response = client.get("/api/teacher/students/student_001")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "student_001"
    assert "overall_mastery" in data
    assert "subject_masteries" in data
    assert "weak_topics" in data

def test_api_get_teacher_topics():
    response = client.get("/api/teacher/topics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert data[0]["topic"] == "Process Scheduling"

def test_api_get_topic_detail():
    response = client.get("/api/teacher/topics/topic_os_sched")
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Process Scheduling"
    assert "mastery_distribution" in data
    assert "struggling_students" in data

def test_api_get_teacher_assessments():
    response = client.get("/api/teacher/assessments")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "most_difficult_question" in data[0]

def test_api_get_teacher_recommendations():
    response = client.get("/api/teacher/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["priority"] == "HIGH"
    assert "why_evidence" in data[0]
    assert "recommended_action" in data[0]

def test_api_create_teaching_activity():
    payload = {
        "topic": "Process Scheduling",
        "subject": "Operating Systems",
        "activity_type": "revision_practice",
        "target_student_ids": ["student_001", "student_005", "student_008"],
        "question_count": 5,
        "difficulty": "adaptive"
    }
    response = client.post("/api/teacher/activities", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Process Scheduling"
    assert data["question_count"] == 5
    assert data["status"] == "created"
    assert "id" in data

def test_api_teacher_health():
    response = client.get("/api/teacher/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
