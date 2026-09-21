import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_student_login():
    response = client.post("/api/auth/login", json={
        "email": "student@learnsync.ai",
        "password": "student123",
        "role": "student"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert data["user"]["role"] == "student"
    assert data["user"]["name"] == "Santhosh"

def test_valid_faculty_login():
    response = client.post("/api/auth/login", json={
        "email": "faculty@learnsync.ai",
        "password": "faculty123",
        "role": "faculty"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert data["user"]["role"] == "faculty"
    assert data["user"]["name"] == "Prof. R. Sharma"

def test_invalid_password():
    response = client.post("/api/auth/login", json={
        "email": "student@learnsync.ai",
        "password": "wrongpassword",
        "role": "student"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_invalid_role_mismatch():
    response = client.post("/api/auth/login", json={
        "email": "student@learnsync.ai",
        "password": "student123",
        "role": "faculty"
    })
    assert response.status_code == 401

def test_missing_field_validation():
    response = client.post("/api/auth/login", json={
        "email": "student@learnsync.ai"
    })
    assert response.status_code == 422
