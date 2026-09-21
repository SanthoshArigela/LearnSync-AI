import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_assessment_generate():
    payload = {
        "subject": "Computer Networks",
        "topic": "TCP",
        "difficulty": "adaptive",
        "question_count": 5
    }
    response = client.post("/api/assessment/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) > 0
    assert data["subject"] == "Computer Networks"

def test_assessment_evaluate():
    payload = {
        "assessment_id": "ass_test_101",
        "subject": "Computer Networks",
        "topic": "TCP",
        "difficulty": "medium",
        "submissions": [
            {
                "question_id": "q1",
                "question_text": "Which protocol provides reliable communication?",
                "selected_key": "B",
                "correct_key": "B",
                "topic": "TCP",
                "subtopic": "TCP basics",
                "explanation": "TCP is reliable."
            },
            {
                "question_id": "q2",
                "question_text": "Which sequence is used for connection release?",
                "selected_key": "A",
                "correct_key": "B",
                "topic": "TCP",
                "subtopic": "TCP connection termination",
                "explanation": "TCP release uses FIN-ACK."
            }
        ],
        "adaptive_path": ["Medium (✓)", "Hard (✗)"]
    }
    response = client.post("/api/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 1
    assert data["total"] == 2
    assert data["percentage"] == 50
    assert "TCP connection termination" in data["needs_practice"]
    assert len(data["mistakes"]) == 1
