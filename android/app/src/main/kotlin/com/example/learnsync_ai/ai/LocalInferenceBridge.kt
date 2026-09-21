package com.example.learnsync_ai.ai

import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel

/**
 * MethodChannel bridge handler for Flutter ↔ Android NPU & local AI capability queries.
 */
class LocalInferenceBridge(private val detector: DeviceCapabilityDetector = DeviceCapabilityDetector()) : MethodChannel.MethodCallHandler {

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "getDeviceCapabilities" -> {
                try {
                    val capabilities = detector.detectCapabilities()
                    result.success(capabilities)
                } catch (e: Exception) {
                    result.error("CAPABILITY_ERROR", "Failed to detect device capabilities: ${e.message}", null)
                }
            }
            "isNpuAvailable" -> {
                try {
                    val capabilities = detector.detectCapabilities()
                    val npuAvailable = capabilities["npu_available"] as? Boolean ?: false
                    result.success(npuAvailable)
                } catch (e: Exception) {
                    result.success(false)
                }
            }
            "getLocalModelStatus" -> {
                try {
                    val capabilities = detector.detectCapabilities()
                    result.success(capabilities["local_model_status"])
                } catch (e: Exception) {
                    result.success("Missing")
                }
            }
            else -> {
                result.notImplemented()
            }
        }
    }
}
