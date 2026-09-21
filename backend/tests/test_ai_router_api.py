import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_router_service import AIRouterService

client = TestClient(app)

def test_get_ai_status_default():
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_provider" in data
    assert "local_available" in data
    assert "gemini_available" in data
    assert data["offline_ready"] is True
    assert "capabilities" in data

def test_get_ai_status_forced_modes():
    modes = ["auto", "local", "gemini", "fallback"]
    for m in modes:
        response = client.get(f"/api/ai/status?mode={m}")
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == m

def test_set_ai_mode_endpoint():
    payload = {"mode": "fallback"}
    response = client.post("/api/ai/mode", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "fallback"
    assert data["active_provider"] == "fallback"

def test_ai_router_service_resolution():
    router = AIRouterService()
    p_fallback = router.resolve_provider("fallback")
    assert p_fallback.provider_name == "fallback"

    p_auto = router.resolve_provider("auto")
    assert p_auto.provider_name in ["gemini", "local_npu", "fallback"]

def test_no_secrets_in_ai_status():
    response = client.get("/api/ai/status")
    data = response.json()
    raw_str = str(data)
    assert "GEMINI_API_KEY" not in raw_str
    assert "key=" not in raw_str
    assert "secret" not in raw_str.lower()
