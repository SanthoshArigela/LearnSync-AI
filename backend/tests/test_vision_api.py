import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_vision_analyze_success():
    payload = {
        "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBD...",
        "student_context": {
            "student_name": "Santhosh",
            "degree": "B.Tech CSE",
            "current_subject": "Computer Networks",
            "current_topic": "TCP"
        }
    }
    response = client.post("/api/vision/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "extracted" in data
    assert data["extracted"]["detected"] is True
    assert "question" in data["extracted"]
    assert "topic" in data["extracted"]

def test_vision_analyze_fallback():
    payload = {
        "image_base64": "sample_short_b64",
    }
    response = client.post("/api/vision/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["extracted"]["question"] is not None
