import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../core/constants/api_config.dart';
import '../models/learning_models.dart';

class LearningService {
  static final LearningService _instance = LearningService._internal();
  factory LearningService() => _instance;
  LearningService._internal();

  LearningProfile _cachedProfile = _buildDefaultProfile();

  static LearningProfile get currentProfile => _instance._cachedProfile;

  static LearningProfile _buildDefaultProfile() {
    final cnTopics = [
      const TopicMastery(
        subject: "Computer Networks",
        topic: "Computer Networks",
        subtopic: "TCP Basics",
        masteryScore: 95,
        attempts: 10,
        correct: 9,
        incorrect: 1,
        trend: "improving",
        status: "strong",
      ),
      const TopicMastery(
        subject: "Computer Networks",
        topic: "Computer Networks",
        subtopic: "TCP Handshake",
        masteryScore: 75,
        attempts: 8,
        correct: 6,
        incorrect: 2,
        trend: "stable",
        status: "moderate",
      ),
      const TopicMastery(
        subject: "Computer Networks",
        topic: "Computer Networks",
        subtopic: "TCP Connection Termination",
        masteryScore: 42,
        attempts: 7,
        correct: 3,
        incorrect: 4,
        trend: "declining",
        status: "needs_practice",
      ),
    ];

    final dsTopics = [
      const TopicMastery(
        subject: "Data Structures",
        topic: "Data Structures",
        subtopic: "Arrays & Lists",
        masteryScore: 92,
        attempts: 12,
        correct: 11,
        incorrect: 1,
        trend: "improving",
        status: "strong",
      ),
      const TopicMastery(
        subject: "Data Structures",
        topic: "Data Structures",
        subtopic: "Binary Trees",
        masteryScore: 60,
        attempts: 5,
        correct: 3,
        incorrect: 2,
        trend: "stable",
        status: "moderate",
      ),
    ];

    final dbTopics = [
      const TopicMastery(
        subject: "DBMS",
        topic: "DBMS",
        subtopic: "SQL & Normalization",
        masteryScore: 85,
        attempts: 10,
        correct: 8,
        incorrect: 2,
        trend: "improving",
        status: "moderate",
      ),
      const TopicMastery(
        subject: "DBMS",
        topic: "DBMS",
        subtopic: "Transactions & Locking",
        masteryScore: 58,
        attempts: 6,
        correct: 3,
        incorrect: 3,
        trend: "declining",
        status: "needs_practice",
      ),
    ];

    final osTopics = [
      const TopicMastery(
        subject: "Operating Systems",
        topic: "Operating Systems",
        subtopic: "Process Scheduling",
        masteryScore: 45,
        attempts: 8,
        correct: 3,
        incorrect: 5,
        trend: "declining",
        status: "needs_practice",
      ),
      const TopicMastery(
        subject: "Operating Systems",
        topic: "Operating Systems",
        subtopic: "Threads & Memory",
        masteryScore: 70,
        attempts: 7,
        correct: 5,
        incorrect: 2,
        trend: "stable",
        status: "moderate",
      ),
    ];

    final subjects = {
      "Computer Networks": SubjectMastery(
        subject: "Computer Networks",
        overallMastery: 82,
        topics: cnTopics,
      ),
      "Data Structures": SubjectMastery(
        subject: "Data Structures",
        overallMastery: 76,
        topics: dsTopics,
      ),
      "DBMS": SubjectMastery(
        subject: "DBMS",
        overallMastery: 71,
        topics: dbTopics,
      ),
      "Operating Systems": SubjectMastery(
        subject: "Operating Systems",
        overallMastery: 58,
        topics: osTopics,
      ),
    };

    const nextBest = LearningRecommendation(
      id: "rec_tcp_1",
      title: "Revise TCP Connection Termination",
      subject: "Computer Networks",
      topic: "Computer Networks",
      subtopic: "TCP Connection Termination",
      reason: "You've struggled with this topic in recent assessments.",
      priority: "high",
      action: "revision",
      estimatedTimeMinutes: 10,
      difficulty: "easy",
    );

    const recs = [
      nextBest,
      LearningRecommendation(
        id: "rec_os_1",
        title: "Practice Process Scheduling",
        subject: "Operating Systems",
        topic: "Operating Systems",
        subtopic: "Process Scheduling",
        reason: "Performance in Process Scheduling is below 60%.",
        priority: "high",
        action: "practice",
        estimatedTimeMinutes: 15,
        difficulty: "medium",
      ),
      LearningRecommendation(
        id: "rec_db_1",
        title: "Review DBMS Transactions",
        subject: "DBMS",
        topic: "DBMS",
        subtopic: "Transactions & Locking",
        reason: "Moderate performance needing reinforcement.",
        priority: "medium",
        action: "revision",
        estimatedTimeMinutes: 10,
        difficulty: "medium",
      ),
    ];

    return LearningProfile(
      studentId: "student_001",
      overallMastery: 78,
      strongTopics: ["TCP Basics", "Arrays & Lists"],
      moderateTopics: ["TCP Handshake", "Binary Trees", "SQL & Normalization", "Threads & Memory"],
      weakTopics: ["TCP Connection Termination", "Transactions & Locking", "Process Scheduling"],
      subjects: subjects,
      trends: [
        {"subject": "Computer Networks", "trend": "improving"},
        {"subject": "Operating Systems", "trend": "declining"},
      ],
      recommendations: recs,
      nextBestAction: nextBest,
    );
  }

  Future<LearningProfile> fetchProfile() async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.learningProfileEndpoint}');
      final response = await http.get(uri).timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _cachedProfile = LearningProfile.fromJson(data);
        return _cachedProfile;
      }
    } catch (e) {
      if (kDebugMode) {
        print('Using cached/offline learning profile due to fetch exception: $e');
      }
    }
    return _cachedProfile;
  }

  Future<LearningProfile> updateFromAssessment({
    required String subject,
    required String topic,
    required int percentage,
    required List<Map<String, dynamic>> submissions,
  }) async {
    // 1. Try updating via backend API
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.learningAnalyzeEndpoint}');
      final body = json.encode({
        "student_id": _cachedProfile.studentId,
        "subject": subject,
        "topic": topic,
        "percentage": percentage,
        "submissions": submissions,
      });

      final response = await http.post(
        uri,
        headers: {"Content-Type": "application/json"},
        body: body,
      ).timeout(ApiConfig.requestTimeout);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['profile'] != null) {
          _cachedProfile = LearningProfile.fromJson(data['profile']);
          return _cachedProfile;
        }
      }
    } catch (e) {
      if (kDebugMode) {
        print('Backend analyze API unavailable ($e), updating profile locally.');
      }
    }

    // 2. Local deterministic fallback calculation
    _applyLocalAssessmentUpdate(subject, topic, percentage, submissions);
    return _cachedProfile;
  }

  void _applyLocalAssessmentUpdate(
    String subject,
    String topic,
    int percentage,
    List<Map<String, dynamic>> submissions,
  ) {
    final existingSubjects = Map<String, SubjectMastery>.from(_cachedProfile.subjects);
    SubjectMastery currentSubj = existingSubjects[subject] ??
        SubjectMastery(subject: subject, overallMastery: percentage, topics: []);

    List<TopicMastery> topics = List<TopicMastery>.from(currentSubj.topics);

    // Group submissions by subtopic
    Map<String, Map<String, int>> subtopicStats = {};
    for (var sub in submissions) {
      String st = (sub['subtopic'] as String?) ?? topic;
      if (!subtopicStats.containsKey(st)) {
        subtopicStats[st] = {'correct': 0, 'total': 0};
      }
      subtopicStats[st]!['total'] = subtopicStats[st]!['total']! + 1;
      if (sub['selected_key'] == sub['correct_key']) {
        subtopicStats[st]!['correct'] = subtopicStats[st]!['correct']! + 1;
      }
    }

    if (subtopicStats.isEmpty) {
      subtopicStats[topic] = {'correct': (percentage / 100 * 5).round(), 'total': 5};
    }

    subtopicStats.forEach((stName, stats) {
      int recentSubScore = stats['total']! > 0
          ? ((stats['correct']! / stats['total']!) * 100).round()
          : percentage;

      int idx = topics.indexWhere((t) => t.subtopic.toLowerCase() == stName.toLowerCase());
      if (idx >= 0) {
        final old = topics[idx];
        int newAttempts = old.attempts + stats['total']!;
        int newCorrect = old.correct + stats['correct']!;
        int newIncorrect = old.incorrect + (stats['total']! - stats['correct']!);

        // Formula: min(100, round(0.6 * recent_score + 0.4 * historical_accuracy))
        double historicalAccuracy = (newCorrect / newAttempts) * 100;
        int newMastery = ((0.6 * recentSubScore) + (0.4 * historicalAccuracy)).round().clamp(0, 100);

        String newStatus = newMastery >= 90
            ? 'strong'
            : (newMastery >= 60 ? 'moderate' : 'needs_practice');

        String newTrend = recentSubScore > old.masteryScore ? 'improving' : (recentSubScore < old.masteryScore ? 'declining' : 'stable');

        topics[idx] = TopicMastery(
          subject: subject,
          topic: topic,
          subtopic: old.subtopic,
          masteryScore: newMastery,
          attempts: newAttempts,
          correct: newCorrect,
          incorrect: newIncorrect,
          trend: newTrend,
          status: newStatus,
          lastPracticedAt: DateTime.now().toIso8601String(),
        );
      } else {
        int newMastery = recentSubScore;
        String newStatus = newMastery >= 90
            ? 'strong'
            : (newMastery >= 60 ? 'moderate' : 'needs_practice');

        topics.add(TopicMastery(
          subject: subject,
          topic: topic,
          subtopic: stName,
          masteryScore: newMastery,
          attempts: stats['total']!,
          correct: stats['correct']!,
          incorrect: stats['total']! - stats['correct']!,
          trend: 'improving',
          status: newStatus,
          lastPracticedAt: DateTime.now().toIso8601String(),
        ));
      }
    });

    int updatedSubjMastery = topics.isNotEmpty
        ? (topics.fold<int>(0, (sum, t) => sum + t.masteryScore) / topics.length).round()
        : percentage;

    existingSubjects[subject] = SubjectMastery(
      subject: subject,
      overallMastery: updatedSubjMastery,
      topics: topics,
    );

    int updatedOverall = existingSubjects.isNotEmpty
        ? (existingSubjects.values.fold<int>(0, (sum, s) => sum + s.overallMastery) / existingSubjects.length).round()
        : percentage;

    List<TopicMastery> allTopics = [];
    existingSubjects.values.forEach((s) => allTopics.addAll(s.topics));

    List<String> strong = allTopics.where((t) => t.status == 'strong').map((t) => t.subtopic).toList();
    List<String> moderate = allTopics.where((t) => t.status == 'moderate').map((t) => t.subtopic).toList();
    List<String> weak = allTopics.where((t) => t.status == 'needs_practice').map((t) => t.subtopic).toList();

    // Re-generate next best action and recommendations
    LearningRecommendation? nextBest;
    List<LearningRecommendation> recs = [];

    if (weak.isNotEmpty) {
      final targetWeak = weak.first;
      nextBest = LearningRecommendation(
        id: "rec_dynamic_1",
        title: "Take a Medium $targetWeak assessment",
        subject: subject,
        topic: topic,
        subtopic: targetWeak,
        reason: "You have improved in $targetWeak! Take a Medium assessment to lock in mastery.",
        priority: "medium",
        action: "assessment",
        estimatedTimeMinutes: 15,
        difficulty: "medium",
      );
      recs.add(nextBest);
    } else {
      nextBest = LearningRecommendation(
        id: "rec_dynamic_2",
        title: "Challenge Assessment: $topic",
        subject: subject,
        topic: topic,
        reason: "Great performance across all topics! Try an advanced assessment.",
        priority: "low",
        action: "assessment",
        estimatedTimeMinutes: 15,
        difficulty: "hard",
      );
      recs.add(nextBest);
    }

    _cachedProfile = LearningProfile(
      studentId: _cachedProfile.studentId,
      overallMastery: updatedOverall,
      strongTopics: strong,
      moderateTopics: moderate,
      weakTopics: weak,
      subjects: existingSubjects,
      trends: [
        {"subject": subject, "trend": "improving"},
      ],
      recommendations: recs,
      nextBestAction: nextBest,
    );
  }
}
