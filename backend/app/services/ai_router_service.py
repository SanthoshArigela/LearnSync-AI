from typing import Dict, Any, Optional
from ..core.config import settings
from ..providers.local_provider import LocalAIProvider
from ..providers.gemini_provider import GeminiProvider
from ..providers.fallback_provider import FallbackProvider
from ..providers.ai_provider import AIProvider

class AIRouterService:
    """
    Centralized AI Routing & Capability Orchestrator for LearnSync AI Engine.
    Intelligently routes requests: Local/On-Device NPU -> Gemini Cloud -> Deterministic Offline Fallback.
    Never exposes secrets or credentials.
    """

    def __init__(self, force_local_available: bool = False, simulated_npu: bool = False):
        self.local_provider = LocalAIProvider(
            force_available=force_local_available,
            simulated_npu=simulated_npu
        )
        self.gemini_provider = GeminiProvider()
        self.fallback_provider = FallbackProvider()

    def get_effective_mode(self, mode_override: Optional[str] = None) -> str:
        mode = (mode_override or settings.AI_PROVIDER_MODE or "auto").lower()
        if mode not in ["auto", "local", "gemini", "fallback"]:
            mode = "auto"
        return mode

    def resolve_provider(self, mode_override: Optional[str] = None) -> AIProvider:
        mode = self.get_effective_mode(mode_override)

        if mode == "local":
            if self.local_provider.is_available:
                return self.local_provider
            # If requested local but local model/runtime is missing, fallback safely
            if self.gemini_provider.is_available:
                return self.gemini_provider
            return self.fallback_provider

        elif mode == "gemini":
            if self.gemini_provider.is_available:
                return self.gemini_provider
            return self.fallback_provider

        elif mode == "fallback":
            return self.fallback_provider

        else:  # 'auto' mode
            if self.local_provider.is_available:
                return self.local_provider
            if self.gemini_provider.is_available:
                return self.gemini_provider
            return self.fallback_provider

    def get_ai_status(self, mode_override: Optional[str] = None) -> Dict[str, Any]:
        mode = self.get_effective_mode(mode_override)
        active_provider = self.resolve_provider(mode)

        local_meta = self.local_provider.get_metadata()

        api_key = settings.GEMINI_API_KEY
        gemini_configured = bool(api_key and api_key.strip() and api_key != "your_gemini_api_key_here")

        return {
            "mode": mode,
            "active_provider": active_provider.provider_name,
            "active_model": active_provider.model_name,
            "gemini_configured": gemini_configured,
            "gemini_available": self.gemini_provider.is_available,
            "gemini_provider_available": self.gemini_provider.is_available,
            "assessment_provider_available": self.gemini_provider.is_available or True,
            "vision_provider_available": self.gemini_provider.is_available or True,
            "configured_model_name": settings.GEMINI_MODEL or "gemini-3.5-flash-lite",
            "last_provider_error_category": None,
            "local_available": self.local_provider.is_available,
            "local_runtime": local_meta.get("runtime", "Local CPU Fallback"),
            "hardware_acceleration": self.local_provider.hardware_acceleration,
            "device_ready": self.local_provider.device_ready,
            "fallback_available": True,
            "offline_ready": True,
            "capabilities": {
                "chat": active_provider.supports_chat,
                "vision": self.gemini_provider.supports_vision or True,
                "assessment": active_provider.supports_assessment,
                "offline": True,
            },
            "device_info": {
                "device": "LearnSync Device Platform",
                "ai_runtime": local_meta.get("runtime", "Local Runtime"),
                "accelerator": "Available" if self.local_provider.hardware_acceleration else "Unavailable",
                "npu_status": "Ready" if self.local_provider.hardware_acceleration else "Not Detected",
                "local_model": "Installed" if self.local_provider.is_available else "Missing",
                "cloud_ai": "Available" if self.gemini_provider.is_available else "Unavailable",
                "offline_mode": "Ready"
            }
        }

