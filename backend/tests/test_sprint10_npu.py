import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.providers.local_inference_runtime import LocalInferenceRuntime
from app.providers.local_provider import LocalAIProvider
from app.services.ai_router_service import AIRouterService

client = TestClient(app)

def test_local_inference_runtime_missing_model():
    runtime = LocalInferenceRuntime(force_available=False, simulated_npu=False)
    assert runtime.is_model_installed is False
    assert runtime.is_npu_available is False
    assert runtime.hardware_acceleration is False
    assert "Model Not Installed" in runtime.runtime_name
    assert runtime.is_available is False

def test_local_inference_runtime_force_available():
    runtime = LocalInferenceRuntime(force_available=True, simulated_npu=False)
    assert runtime.is_model_installed is True
    assert runtime.is_available is True
    assert runtime.hardware_acceleration is False
    assert "Local CPU" in runtime.runtime_name

def test_local_inference_runtime_simulated_npu():
    runtime = LocalInferenceRuntime(force_available=True, simulated_npu=True)
    assert runtime.is_npu_available is True
    assert runtime.hardware_acceleration is True
    assert "Snapdragon NPU" in runtime.runtime_name

@pytest.mark.asyncio
async def test_local_ai_provider_response():
    provider = LocalAIProvider(force_available=True, simulated_npu=False)
    assert provider.provider_name == "local"
    assert provider.is_available is True

    res = await provider.generate_response(
        messages=[{"role": "user", "content": "Why does TCP use a three-way handshake?"}],
        explanation_mode="simple"
    )
    assert "answer" in res
    assert res["provider_used"] == "local_cpu"
    assert res["execution_type"] == "LOCAL DEMO / FALLBACK"

def test_ai_router_service_routing_modes():
    # Test Auto mode
    router = AIRouterService(force_local_available=False, simulated_npu=False)
    status_auto = router.get_ai_status(mode_override="auto")
    assert status_auto["mode"] == "auto"
    assert "capabilities" in status_auto
    assert "device_info" in status_auto

    # Test Local override mode
    status_local = router.get_ai_status(mode_override="local")
    assert status_local["mode"] == "local"

    # Test Gemini override mode
    status_gemini = router.get_ai_status(mode_override="gemini")
    assert status_gemini["mode"] == "gemini"

    # Test Fallback override mode
    status_fallback = router.get_ai_status(mode_override="fallback")
    assert status_fallback["mode"] == "fallback"
    assert status_fallback["active_provider"] in ["fallback", "deterministic"]

def test_ai_status_endpoint():
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert "active_provider" in data
    assert "local_available" in data
    assert "local_runtime" in data
    assert "hardware_acceleration" in data
    assert "device_ready" in data
    assert "capabilities" in data
    assert "device_info" in data

def test_ai_status_demo_npu_simulation():
    response = client.get("/api/ai/status?force_local=true&simulated_npu=true")
    assert response.status_code == 200
    data = response.json()
    assert data["local_available"] is True
    assert data["hardware_acceleration"] is True
    assert "Snapdragon NPU" in data["local_runtime"]
    assert data["device_info"]["npu_status"] == "Ready"

def test_ai_status_no_secret_leakage():
    response = client.get("/api/ai/status")
    data_str = str(response.json())
    assert "api_key" not in data_str.lower()
    assert "gemini_api_key" not in data_str.lower()
    assert "secret" not in data_str.lower()
