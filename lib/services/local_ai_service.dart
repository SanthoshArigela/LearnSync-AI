import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

/// Models hardware runtime capabilities reported by Android device or backend.
class LocalAiCapability {
  final String activeProvider;
  final String activeModel;
  final String localRuntime;
  final bool hardwareAcceleration;
  final bool localAvailable;
  final bool geminiAvailable;
  final bool fallbackAvailable;
  final bool offlineReady;
  final String npuStatus;
  final String localModelStatus;

  LocalAiCapability({
    required this.activeProvider,
    required this.activeModel,
    required this.localRuntime,
    required this.hardwareAcceleration,
    required this.localAvailable,
    required this.geminiAvailable,
    required this.fallbackAvailable,
    required this.offlineReady,
    required this.npuStatus,
    required this.localModelStatus,
  });

  factory LocalAiCapability.fromJson(Map<String, dynamic> json) {
    final deviceInfo = json['device_info'] as Map<String, dynamic>? ?? {};
    return LocalAiCapability(
      activeProvider: json['active_provider'] ?? 'fallback',
      activeModel: json['active_model'] ?? 'LearnSync Fallback Engine',
      localRuntime: json['local_runtime'] ?? 'Local CPU Fallback',
      hardwareAcceleration: json['hardware_acceleration'] ?? false,
      localAvailable: json['local_available'] ?? false,
      geminiAvailable: json['gemini_available'] ?? false,
      fallbackAvailable: json['fallback_available'] ?? true,
      offlineReady: json['offline_ready'] ?? true,
      npuStatus: deviceInfo['npu_status'] ?? 'Not Detected',
      localModelStatus: deviceInfo['local_model'] ?? 'Missing',
    );
  }

  factory LocalAiCapability.defaultFallback() {
    return LocalAiCapability(
      activeProvider: 'fallback',
      activeModel: 'LearnSync Local Educational Engine',
      localRuntime: 'Local CPU Fallback',
      hardwareAcceleration: false,
      localAvailable: false,
      geminiAvailable: false,
      fallbackAvailable: true,
      offlineReady: true,
      npuStatus: 'Not Detected',
      localModelStatus: 'Missing',
    );
  }
}

class LocalAiService {
  static const MethodChannel _npuChannel = MethodChannel('com.learnsync.ai/npu_bridge');

  /// Safe query to native Android MethodChannel for hardware capabilities.
  Future<Map<String, dynamic>> getNativeDeviceCapabilities() async {
    try {
      final Map<dynamic, dynamic>? result =
          await _npuChannel.invokeMethod('getDeviceCapabilities');
      if (result != null) {
        return Map<String, dynamic>.from(result);
      }
    } on MissingPluginException {
      // Running on non-Android platform (e.g. desktop/web testing)
    } catch (e) {
      // Platform exception caught safely
    }
    return {
      'device': 'LearnSync Platform',
      'npu_available': false,
      'npu_status': 'Not Detected',
      'local_model_installed': false,
      'local_model_status': 'Missing',
      'runtime_name': 'Local CPU Fallback'
    };
  }

  /// Fetches unified AI status from backend API.
  Future<LocalAiCapability> fetchAiStatus({String? modeOverride}) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}/api/ai/status${modeOverride != null ? '?mode=$modeOverride' : ''}');
      final response = await http.get(uri).timeout(const Duration(seconds: 4));
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return LocalAiCapability.fromJson(data);
      }
    } catch (e) {
      // Network/offline fallback
    }
    return LocalAiCapability.defaultFallback();
  }

  /// Switches active provider mode override (auto, local, gemini, fallback).
  Future<LocalAiCapability> setAiMode(String mode, {bool forceLocal = false, bool simulatedNpu = false}) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}/api/ai/mode');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'mode': mode,
          'force_local': forceLocal,
          'simulated_npu': simulatedNpu,
        }),
      ).timeout(const Duration(seconds: 4));
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return LocalAiCapability.fromJson(data);
      }
    } catch (e) {
      // Fallback
    }
    return LocalAiCapability.defaultFallback();
  }
}
