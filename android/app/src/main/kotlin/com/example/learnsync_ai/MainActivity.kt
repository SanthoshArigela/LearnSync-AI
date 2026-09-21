package com.example.learnsync_ai

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import com.example.learnsync_ai.ai.LocalInferenceBridge

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.learnsync.ai/npu_bridge"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler(LocalInferenceBridge())
    }
}
