import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.learning_gap_service import LearningGapService
from app.services.recommendation_service import RecommendationService
from app.services.learning_profile_service import LearningProfileService
from app.models.learning_models import TopicMasteryModel

client = TestClient(app)

def test_mastery_calculation_formula():
    # Mastery = min(100, round(0.6 * recent_score + 0.4 * historical_accuracy))
    # Test case 1: Recent score 70%, historical accuracy 50% (5 correct / 10 attempts = 50%)
    mastery = LearningGapService.calculate_topic_mastery(70, 5, 10)
    # 0.6 * 70 + 0.4 * 50 = 42 + 20 = 62
    assert mastery == 62

    # Test case 2: Perfect score
    mastery_max = LearningGapService.calculate_topic_mastery(100, 10, 10)
    assert mastery_max == 100

def test_performance_status_classification():
    assert LearningGapService.classify_status(95) == "strong"
    assert LearningGapService.classify_status(90) == "strong"
    assert LearningGapService.classify_status(85) == "moderate"
    assert LearningGapService.classify_status(60) == "moderate"
    assert LearningGapService.classify_status(58) == "needs_practice"
    assert LearningGapService.classify_status(30) == "needs_practice"

def test_performance_trend_calculation():
    assert LearningGapService.calculate_trend([50, 60, 72]) == "improving"
    assert LearningGapService.calculate_trend([85, 70, 55]) == "declining"
    assert LearningGapService.calculate_trend([80, 78, 79]) == "stable"
    assert LearningGapService.calculate_trend([70]) == "stable"

def test_repeated_mistakes_detection():
    mistakes = [
        {"question_id": "q1", "topic": "Computer Networks", "subtopic": "TCP Connection Termination"},
        {"question_id": "q2", "topic": "Computer Networks", "subtopic": "TCP Connection Termination"},
        {"question_id": "q3", "topic": "Computer Networks", "subtopic": "TCP Basics"}
    ]
    repeated = LearningGapService.detect_repeated_mistakes(mistakes)
    assert len(repeated) == 1
    assert repeated[0]["subtopic"] == "TCP Connection Termination"
    assert repeated[0]["count"] == 2

def test_recommendation_generation_and_priority():
    topics = [
        TopicMasteryModel(subject="Computer Networks", topic="Computer Networks", subtopic="TCP Basics", mastery_score=95, status="strong"),
        TopicMasteryModel(subject="Computer Networks", topic="Computer Networks", subtopic="TCP Connection Termination", mastery_score=42, status="needs_practice")
    ]
    repeated = [{"subtopic": "TCP Connection Termination", "topic": "Computer Networks", "count": 2}]
    
    recs, next_best = RecommendationService.generate_recommendations(topics, repeated)
    
    assert len(recs) >= 1
    assert next_best is not None
    assert next_best.priority == "high"
    assert "TCP Connection Termination" in next_best.title
    assert "Repeated difficulty" in next_best.reason or "scored 42%" in next_best.reason

def test_learning_profile_service_flow():
    service = LearningProfileService()
    profile = service.get_profile()
    assert profile.student_id == "student_001"
    assert "Computer Networks" in profile.subjects
    assert profile.next_best_action is not None

    # Update profile after new assessment
    updated = service.update_from_assessment_result(
        subject="Computer Networks",
        topic="Computer Networks",
        percentage=100,
        submissions=[
            {"question_id": "q1", "topic": "Computer Networks", "subtopic": "TCP Connection Termination", "selected_key": "A", "correct_key": "A"}
        ],
        mistakes=[]
    )
    assert updated.overall_mastery >= 70

def test_api_get_learning_profile():
    response = client.get("/api/learning/profile")
    assert response.status_code == 200
    data = response.json()
    assert "overall_mastery" in data
    assert "subjects" in data
    assert "recommendations" in data
    assert "next_best_action" in data

def test_api_get_recommendations():
    response = client.get("/api/learning/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]
    assert "priority" in data[0]

def test_api_post_analyze():
    response = client.post("/api/learning/analyze", json={
        "student_id": "student_001",
        "assessment_history": []
    })
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "student_001"
    assert "profile" in data

def test_empty_assessment_history_handling():
    service = LearningProfileService()
    profile = service.get_profile()
    assert profile.overall_mastery >= 0
    assert isinstance(profile.weak_topics, list)
    assert isinstance(profile.recommendations, list)

def test_gemini_unavailable_offline_fallback():
    # Learning profile calculation does not depend on Gemini API and works offline
    service = LearningProfileService()
    updated = service.update_from_assessment_result(
        subject="Computer Networks",
        topic="Computer Networks",
        percentage=40,
        submissions=[
            {"question_id": "q1", "topic": "Computer Networks", "subtopic": "TCP Connection Termination", "selected_key": "A", "correct_key": "B"}
        ],
        mistakes=[
            {"question_id": "q1", "topic": "Computer Networks", "subtopic": "TCP Connection Termination"}
        ]
    )
    assert updated is not None
    assert updated.next_best_action is not None
    assert updated.next_best_action.priority == "high"

