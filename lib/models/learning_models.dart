class TopicMastery {
  final String subject;
  final String topic;
  final String subtopic;
  final int masteryScore;
  final int attempts;
  final int correct;
  final int incorrect;
  final String trend; // 'improving' | 'stable' | 'declining'
  final String status; // 'strong' | 'moderate' | 'needs_practice'
  final String? lastPracticedAt;

  const TopicMastery({
    required this.subject,
    required this.topic,
    required this.subtopic,
    required this.masteryScore,
    required this.attempts,
    required this.correct,
    required this.incorrect,
    this.trend = 'stable',
    this.status = 'needs_practice',
    this.lastPracticedAt,
  });

  factory TopicMastery.fromJson(Map<String, dynamic> json) {
    return TopicMastery(
      subject: json['subject'] ?? '',
      topic: json['topic'] ?? '',
      subtopic: json['subtopic'] ?? json['topic'] ?? '',
      masteryScore: (json['mastery_score'] ?? 0) as int,
      attempts: (json['attempts'] ?? 0) as int,
      correct: (json['correct'] ?? 0) as int,
      incorrect: (json['incorrect'] ?? 0) as int,
      trend: json['trend'] ?? 'stable',
      status: json['status'] ?? 'needs_practice',
      lastPracticedAt: json['last_practiced_at'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'subject': subject,
      'topic': topic,
      'subtopic': subtopic,
      'mastery_score': masteryScore,
      'attempts': attempts,
      'correct': correct,
      'incorrect': incorrect,
      'trend': trend,
      'status': status,
      'last_practiced_at': lastPracticedAt,
    };
  }
}

class SubjectMastery {
  final String subject;
  final int overallMastery;
  final List<TopicMastery> topics;

  const SubjectMastery({
    required this.subject,
    required this.overallMastery,
    required this.topics,
  });

  factory SubjectMastery.fromJson(Map<String, dynamic> json) {
    var rawTopics = json['topics'] as List? ?? [];
    return SubjectMastery(
      subject: json['subject'] ?? '',
      overallMastery: (json['overall_mastery'] ?? 0) as int,
      topics: rawTopics.map((t) => TopicMastery.fromJson(t)).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'subject': subject,
      'overall_mastery': overallMastery,
      'topics': topics.map((t) => t.toJson()).toList(),
    };
  }
}

class LearningRecommendation {
  final String id;
  final String title;
  final String subject;
  final String topic;
  final String? subtopic;
  final String reason;
  final String priority; // 'high' | 'medium' | 'low'
  final String action; // 'revision' | 'practice' | 'tutor' | 'assessment'
  final int estimatedTimeMinutes;
  final String difficulty; // 'easy' | 'medium' | 'hard'

  const LearningRecommendation({
    required this.id,
    required this.title,
    required this.subject,
    required this.topic,
    this.subtopic,
    required this.reason,
    this.priority = 'medium',
    this.action = 'revision',
    this.estimatedTimeMinutes = 10,
    this.difficulty = 'medium',
  });

  factory LearningRecommendation.fromJson(Map<String, dynamic> json) {
    return LearningRecommendation(
      id: json['id'] ?? '',
      title: json['title'] ?? '',
      subject: json['subject'] ?? '',
      topic: json['topic'] ?? '',
      subtopic: json['subtopic'],
      reason: json['reason'] ?? '',
      priority: json['priority'] ?? 'medium',
      action: json['action'] ?? 'revision',
      estimatedTimeMinutes: (json['estimated_time_minutes'] ?? 10) as int,
      difficulty: json['difficulty'] ?? 'medium',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'subject': subject,
      'topic': topic,
      'subtopic': subtopic,
      'reason': reason,
      'priority': priority,
      'action': action,
      'estimated_time_minutes': estimatedTimeMinutes,
      'difficulty': difficulty,
    };
  }
}

class LearningProfile {
  final String studentId;
  final int overallMastery;
  final List<String> strongTopics;
  final List<String> moderateTopics;
  final List<String> weakTopics;
  final Map<String, SubjectMastery> subjects;
  final List<Map<String, dynamic>> trends;
  final List<LearningRecommendation> recommendations;
  final LearningRecommendation? nextBestAction;

  const LearningProfile({
    required this.studentId,
    required this.overallMastery,
    required this.strongTopics,
    required this.moderateTopics,
    required this.weakTopics,
    required this.subjects,
    required this.trends,
    required this.recommendations,
    this.nextBestAction,
  });

  factory LearningProfile.fromJson(Map<String, dynamic> json) {
    var rawStrong = (json['strong_topics'] as List? ?? []).cast<String>();
    var rawMod = (json['moderate_topics'] as List? ?? []).cast<String>();
    var rawWeak = (json['weak_topics'] as List? ?? []).cast<String>();
    
    var rawSubjects = json['subjects'] as Map<String, dynamic>? ?? {};
    Map<String, SubjectMastery> subjMap = {};
    rawSubjects.forEach((k, v) {
      if (v is Map<String, dynamic>) {
        subjMap[k] = SubjectMastery.fromJson(v);
      }
    });

    var rawRecs = json['recommendations'] as List? ?? [];
    List<LearningRecommendation> recList =
        rawRecs.map((r) => LearningRecommendation.fromJson(r as Map<String, dynamic>)).toList();

    LearningRecommendation? nba;
    if (json['next_best_action'] != null && json['next_best_action'] is Map<String, dynamic>) {
      nba = LearningRecommendation.fromJson(json['next_best_action']);
    }

    var rawTrends = (json['trends'] as List? ?? []).map((e) => e as Map<String, dynamic>).toList();

    return LearningProfile(
      studentId: json['student_id'] ?? 'student_001',
      overallMastery: (json['overall_mastery'] ?? 78) as int,
      strongTopics: rawStrong,
      moderateTopics: rawMod,
      weakTopics: rawWeak,
      subjects: subjMap,
      trends: rawTrends,
      recommendations: recList,
      nextBestAction: nba,
    );
  }
}
