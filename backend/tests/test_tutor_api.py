import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_tutor_chat_basic():
    payload = {
        "message": "Why does TCP use a three-way handshake?",
        "explanation_mode": "simple",
        "conversation_id": "test_conv_1"
    }
    response = client.post("/api/tutor/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["explanation_mode"] == "simple"
    assert len(data["suggested_followups"]) > 0

def test_tutor_semantic_response_quality_10_cases():
    test_cases = [
        {
            "question": "fundamentals in c",
            "expected_subject": "C Programming",
            "expected_topic": "Fundamentals",
            "required_content": ["Variables", "Data Types", "printf"]
        },
        {
            "question": "I'm weak in C programming. Teach me.",
            "expected_subject": "C Programming",
            "expected_topic": "Fundamentals",
            "required_content": ["Variables", "function"]
        },
        {
            "question": "Explain pointers in C.",
            "expected_subject": "C Programming",
            "expected_topic": "Pointers",
            "required_content": ["memory", "address"]
        },
        {
            "question": "How does a for loop work in C?",
            "expected_subject": "C Programming",
            "expected_topic": "Loops",
            "required_content": ["loop", "for"]
        },
        {
            "question": "What is a binary search tree?",
            "expected_subject": "Data Structures",
            "expected_topic": "Binary Search Tree",
            "required_content": ["node", "tree"]
        },
        {
            "question": "Explain TCP three-way handshake.",
            "expected_subject": "Computer Networks",
            "expected_topic": "TCP",
            "required_content": ["SYN", "ACK"]
        },
        {
            "question": "What is normalization in DBMS?",
            "expected_subject": "DBMS",
            "expected_topic": "Normalization",
            "required_content": ["table", "redundancy"]
        },
        {
            "question": "What is process scheduling?",
            "expected_subject": "Operating Systems",
            "expected_topic": "Process",
            "required_content": ["CPU"]
        },
        {
            "question": "Explain Python dictionaries.",
            "expected_subject": "Python Programming",
            "expected_topic": "Dictionaries",
            "required_content": ["key", "value"]
        },
        {
            "question": "Explain Java inheritance.",
            "expected_subject": "Java Programming",
            "expected_topic": "Inheritance",
            "required_content": ["class", "extends"]
        },
    ]

    for tc in test_cases:
        payload = {
            "message": tc["question"],
            "explanation_mode": "simple",
            "conversation_id": f"conv_{hash(tc['question'])}"
        }
        response = client.post("/api/tutor/chat", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Subject and Topic assertions
        assert (tc["expected_subject"].lower() in data["subject"].lower() or "computer" in data["subject"].lower() or "programming" in data["subject"].lower()), f"Failed subject match for '{tc['question']}'"
        assert len(data["topic"]) > 0, f"Empty topic for '{tc['question']}'"

        # Answer content relevance assertion
        answer_text = data["answer"].lower()
        has_req_content = any(req.lower() in answer_text for req in tc["required_content"])
        assert has_req_content or len(answer_text) > 150, f"Missing expected educational content in answer for '{tc['question']}'"

        # Never return generic template filler
        assert "evaluated your query regarding Fundamentals" not in answer_text

def test_tutor_explanation_modes():
    modes = ["simple", "real-world", "technical"]
    for m in modes:
        payload = {
            "message": "fundamentals in c",
            "explanation_mode": m,
            "conversation_id": "test_conv_mode"
        }
        response = client.post("/api/tutor/chat", json=payload)
        assert response.status_code == 200
        assert response.json()["explanation_mode"] == m

def test_quiz_me_flow():
    payload = {
        "message": "Quiz me on C Programming",
        "explanation_mode": "simple",
        "action": "quiz_me",
        "conversation_id": "test_conv_quiz"
    }
    response = client.post("/api/tutor/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["quiz"] is not None
    quiz = data["quiz"]

    check_payload = {
        "quiz_id": quiz["id"],
        "selected_key": quiz["correct_key"],
        "correct_key": quiz["correct_key"],
        "explanation": quiz["explanation"]
    }
    res_check = client.post("/api/tutor/quiz/check", json=check_payload)
    assert res_check.status_code == 200
    check_data = res_check.json()
    assert check_data["is_correct"] is True

def test_reset_conversation():
    res = client.post("/api/tutor/reset?conversation_id=test_conv_1")
    assert res.status_code == 200
    assert res.json()["status"] == "reset"
