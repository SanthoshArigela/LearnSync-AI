from typing import List, Dict, Any, Optional
from .ai_provider import AIProvider
from .local_inference_runtime import LocalInferenceRuntime
from ..models.tutor_models import StudentContextModel

class LocalAIProvider(AIProvider):
    """
    Local / On-Device NPU Open-Source AI Provider Architecture.
    Delegates execution to LocalInferenceRuntime for Snapdragon NPU, LiteRT, ONNX, or safe CPU fallback.
    """

    def __init__(self, force_available: bool = False, simulated_npu: bool = False):
        self._runtime = LocalInferenceRuntime(
            force_available=force_available,
            simulated_npu=simulated_npu
        )

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def supports_chat(self) -> bool:
        return True

    @property
    def supports_vision(self) -> bool:
        return False  # Local text SLM; heavy vision OCR falls back to Gemini / local OCR

    @property
    def supports_assessment(self) -> bool:
        return True

    @property
    def supports_offline(self) -> bool:
        return True

    @property
    def is_available(self) -> bool:
        return self._runtime.is_available

    @property
    def model_name(self) -> str:
        return self._runtime.model_name

    @property
    def runtime_name(self) -> str:
        return self._runtime.runtime_name

    @property
    def hardware_acceleration(self) -> bool:
        return self._runtime.hardware_acceleration

    @property
    def device_ready(self) -> bool:
        return self.is_available

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "provider": self.provider_name,
            "runtime": self.runtime_name,
            "model": self.model_name,
            "hardware_acceleration": self.hardware_acceleration,
            "available": self.is_available,
            "device_ready": self.device_ready,
            "offline": True,
            "capabilities": {
                "chat": self.supports_chat,
                "vision": self.supports_vision,
                "assessment": self.supports_assessment,
                "offline": self.supports_offline
            }
        }

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        explanation_mode: str,
        student_context: Optional[StudentContextModel] = None,
        action: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delegates local inference to LocalInferenceRuntime.
        """
        return await self._runtime.run_inference(
            messages=messages,
            explanation_mode=explanation_mode,
            student_context=student_context,
            action=action
        )

