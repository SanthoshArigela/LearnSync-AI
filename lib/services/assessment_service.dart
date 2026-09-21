import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants/api_config.dart';
import '../data/mock/mock_data_service.dart';
import '../models/student_model.dart';

class AssessmentService {
  static final List<AssessmentResult> _history = [];

  static List<AssessmentResult> get history => _history;

  Future<List<Question>> generateAssessmentQuestions({
    required String subject,
    required String topic,
    required String difficulty,
    required int questionCount,
  }) async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/assessment/generate');

    final payload = jsonEncode({
      'subject': subject,
      'topic': topic,
      'difficulty': difficulty,
      'question_count': questionCount,
      'student_context': {
        'student_name': MockDataService.currentStudent.name,
        'degree': MockDataService.currentStudent.degree,
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
        final questionsRaw = data['questions'] as List? ?? [];
        return questionsRaw.map((q) => _parseQuestion(q)).toList();
      }
    } catch (_) {}

    // Fallback question generation
    return MockDataService.cnQuestions.take(questionCount).toList();
  }

  Future<AssessmentResult> evaluateAssessment({
    required String assessmentId,
    required String subject,
    required String topic,
    required String difficulty,
    required List<Map<String, dynamic>> submissions,
    List<String>? adaptivePath,
  }) async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/assessment/evaluate');

    final payload = jsonEncode({
      'assessment_id': assessmentId,
      'subject': subject,
      'topic': topic,
      'difficulty': difficulty,
      'submissions': submissions,
      'adaptive_path': adaptivePath,
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

        final res = AssessmentResult(
          score: data['score'] ?? 0,
          total: data['total'] ?? submissions.length,
          percentage: data['percentage'] ?? 0,
          strongAreas: List<String>.from(data['strong_areas'] ?? []),
          needsPractice: List<String>.from(data['needs_practice'] ?? []),
          aiRecommendation: data['ai_recommendation'] ?? 'Review weak topics.',
        );

        _history.add(res);
        return res;
      }
    } catch (_) {}

    // Fallback deterministic evaluation
    int score = 0;
    for (var sub in submissions) {
      if (sub['selected_key'] == sub['correct_key']) {
        score++;
      }
    }
    final pct = ((score / submissions.length) * 100).toInt();

    final fallbackRes = AssessmentResult(
      score: score,
      total: submissions.length,
      percentage: pct,
      strongAreas: const ['TCP basics', 'DNS'],
      needsPractice: const ['TCP connection termination'],
      aiRecommendation:
          'You may need more practice with TCP connection termination. Spend 10 minutes reviewing this topic before your next assessment.',
    );

    _history.add(fallbackRes);
    return fallbackRes;
  }

  Question _parseQuestion(Map<String, dynamic> json) {
    var optsRaw = json['options'] as List? ?? [];
    List<QuestionOption> options = optsRaw
        .map((o) => QuestionOption(key: o['key'] ?? '', text: o['text'] ?? ''))
        .toList();

    return Question(
      id: json['id'] ?? '',
      text: json['question'] ?? '',
      options: options,
      correctOptionKey: json['correct_key'] ?? 'A',
      explanation: json['explanation'] ?? '',
    );
  }
}
