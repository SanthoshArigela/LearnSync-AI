import 'package:flutter/foundation.dart';

class ApiConfig {
  // Configurable host IP for backend API connection
  static String lanHostIp = '192.168.1.65'; // Host IPv4 LAN IP
  static int port = 8000;

  // Custom override if user passes specific host IP
  static String? customBaseUrl;

  static String get baseUrl {
    if (customBaseUrl != null && customBaseUrl!.isNotEmpty) {
      return customBaseUrl!;
    }
    
    if (kIsWeb) {
      return 'http://127.0.0.1:$port';
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      // Use LAN IP for physical device or 10.0.2.2 for emulator
      return 'http://$lanHostIp:$port';
    } else {
      return 'http://127.0.0.1:$port';
    }
  }

  static const String tutorChatEndpoint = '/api/tutor/chat';
  static const String quizCheckEndpoint = '/api/tutor/quiz/check';
  static const String resetChatEndpoint = '/api/tutor/reset';
  static const String learningProfileEndpoint = '/api/learning/profile';
  static const String learningAnalyzeEndpoint = '/api/learning/analyze';
  static const String recommendationsEndpoint = '/api/learning/recommendations';
  static const String healthEndpoint = '/api/health';

  static const Duration requestTimeout = Duration(seconds: 10);
}
