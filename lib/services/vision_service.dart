import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../core/constants/api_config.dart';
import '../data/mock/mock_data_service.dart';

class ExtractedQuestionResult {
  final bool detected;
  final String question;
  final String topic;
  final String? subtopic;
  final String contentType;
  final double confidence;
  final String? rawOcrText;

  ExtractedQuestionResult({
    required this.detected,
    required this.question,
    required this.topic,
    this.subtopic,
    required this.contentType,
    required this.confidence,
    this.rawOcrText,
  });

  factory ExtractedQuestionResult.fromJson(Map<String, dynamic> json) {
    return ExtractedQuestionResult(
      detected: json['detected'] ?? true,
      question: json['question'] ?? 'Solve: 2x + 5 = 15',
      topic: json['topic'] ?? 'Mathematics',
      subtopic: json['subtopic'],
      contentType: json['content_type'] ?? 'question',
      confidence: (json['confidence'] ?? 0.95).toDouble(),
      rawOcrText: json['raw_ocr_text'],
    );
  }
}

class VisionService {
  Future<ExtractedQuestionResult> analyzeImageBytes(Uint8List bytes) async {
    if (bytes.isEmpty) {
      return _fallbackExtraction(null);
    }

    final base64Image = base64Encode(bytes);
    final url = Uri.parse('${ApiConfig.baseUrl}/api/vision/analyze');

    final payload = jsonEncode({
      'image_base64': base64Image,
      'student_context': {
        'student_name': MockDataService.currentStudent.name,
        'degree': MockDataService.currentStudent.degree,
        'current_subject': 'Computer Networks',
        'current_topic': 'TCP',
      }
    });

    try {
      final response = await http
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: payload,
          )
          .timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['extracted'] != null) {
          return ExtractedQuestionResult.fromJson(data['extracted']);
        }
      }
    } catch (_) {}

    // Controlled offline demo fallback
    return _fallbackExtraction(bytes);
  }

  ExtractedQuestionResult _fallbackExtraction(Uint8List? bytes) {
    return ExtractedQuestionResult(
      detected: true,
      question: 'Solve: 2x + 5 = 15',
      topic: 'Mathematics',
      subtopic: 'Linear Equations',
      contentType: 'equation',
      confidence: 0.96,
      rawOcrText: 'Solve for x: 2x + 5 = 15',
    );
  }
}
