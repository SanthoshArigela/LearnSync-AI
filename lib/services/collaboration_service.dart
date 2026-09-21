import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../core/constants/api_config.dart';

class CollaborationService {
  static final CollaborationService instance = CollaborationService._internal();

  factory CollaborationService() => instance;

  CollaborationService._internal();

  final ValueNotifier<bool> isConnected = ValueNotifier<bool>(true);
  final ValueNotifier<String> lastSyncTime = ValueNotifier<String>('Just now');
  final ValueNotifier<Map<String, dynamic>?> pendingTeacherAction = ValueNotifier<Map<String, dynamic>?>(null);

  Timer? _pollingTimer;
  bool _initialized = false;

  void initialize({String studentId = 'student_001'}) {
    if (_initialized) return;
    _initialized = true;

    // Start background REST polling fallback for teacher actions
    _pollPendingActions(studentId);
    _pollingTimer = Timer.periodic(const Duration(seconds: 5), (_) {
      _pollPendingActions(studentId);
    });
  }

  Future<void> _pollPendingActions(String studentId) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/collaboration/actions/student/$studentId');
      final res = await http.get(url).timeout(const Duration(seconds: 4));

      if (res.statusCode == 200) {
        final List actions = jsonDecode(res.body);
        if (actions.isNotEmpty) {
          final latest = actions.first as Map<String, dynamic>;
          pendingTeacherAction.value = latest;
        }
        isConnected.value = true;
        lastSyncTime.value = _formatTime(DateTime.now());
      }
    } catch (e) {
      // In offline / fallback mode, keep service non-blocking
      isConnected.value = false;
    }
  }

  Future<void> sendStudentEvent({
    required String eventType,
    required String subject,
    required String topic,
    String? subtopic,
    int? score,
    int? mastery,
    String severity = 'HIGH',
    Map<String, dynamic>? payload,
    String studentId = 'student_001',
    String studentName = 'Santhosh K.',
  }) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/collaboration/events');
      final evt = {
        'event_type': eventType,
        'source': 'student',
        'student_id': studentId,
        'student_name': studentName,
        'subject': subject,
        'topic': topic,
        'subtopic': subtopic ?? '',
        'score': score,
        'mastery': mastery,
        'severity': severity,
        'timestamp': _formatTime(DateTime.now()),
        'payload': payload ?? {},
      };

      await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(evt),
      ).timeout(const Duration(seconds: 4));

      lastSyncTime.value = _formatTime(DateTime.now());
      isConnected.value = true;
    } catch (e) {
      if (kDebugMode) {
        print('Collaboration event send fallback: $e');
      }
    }
  }

  Future<void> acknowledgeAction(String actionId, {String studentId = 'student_001'}) async {
    pendingTeacherAction.value = null;
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/collaboration/actions/ack/$actionId?student_id=$studentId');
      await http.post(url).timeout(const Duration(seconds: 3));
    } catch (e) {}
  }

  String _formatTime(DateTime dt) {
    final h = dt.hour.toString().padLeft(2, '0');
    final m = dt.minute.toString().padLeft(2, '0');
    final s = dt.second.toString().padLeft(2, '0');
    return '$h:$m:$s';
  }

  void dispose() {
    _pollingTimer?.cancel();
  }
}
