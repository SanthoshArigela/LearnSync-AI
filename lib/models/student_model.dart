class Student {
  final String id;
  final String name;
  final String degree;
  final String avatarUrl;

  const Student({
    required this.id,
    required this.name,
    required this.degree,
    this.avatarUrl = '',
  });
}

class Subject {
  final String id;
  final String title;
  final int totalTopics;
  final int progressPercentage;
  final String iconName;

  const Subject({
    required this.id,
    required this.title,
    required this.totalTopics,
    required this.progressPercentage,
    required this.iconName,
  });
}

class Topic {
  final String id;
  final String subjectId;
  final String title;
  final int progressPercentage;

  const Topic({
    required this.id,
    required this.subjectId,
    required this.title,
    required this.progressPercentage,
  });
}

class QuestionOption {
  final String key; // A, B, C, D
  final String text;

  const QuestionOption({
    required this.key,
    required this.text,
  });

  factory QuestionOption.fromJson(Map<String, dynamic> json) {
    return QuestionOption(
      key: json['key'] ?? '',
      text: json['text'] ?? '',
    );
  }
}

class QuizData {
  final String id;
  final String question;
  final List<QuestionOption> options;
  final String correctKey;
  final String explanation;

  const QuizData({
    required this.id,
    required this.question,
    required this.options,
    required this.correctKey,
    required this.explanation,
  });

  factory QuizData.fromJson(Map<String, dynamic> json) {
    var optsRaw = json['options'] as List? ?? [];
    List<QuestionOption> opts = optsRaw.map((o) => QuestionOption.fromJson(o)).toList();

    return QuizData(
      id: json['id'] ?? '',
      question: json['question'] ?? '',
      options: opts,
      correctKey: json['correct_key'] ?? 'A',
      explanation: json['explanation'] ?? '',
    );
  }
}

class Question {
  final String id;
  final String text;
  final List<QuestionOption> options;
  final String correctOptionKey;
  final String explanation;

  const Question({
    required this.id,
    required this.text,
    required this.options,
    required this.correctOptionKey,
    required this.explanation,
  });
}

class Assessment {
  final String id;
  final String subjectName;
  final int totalQuestions;
  final String difficulty;
  final int? lastScorePercentage;
  final bool attempted;
  final List<Question> questions;

  const Assessment({
    required this.id,
    required this.subjectName,
    required this.totalQuestions,
    required this.difficulty,
    this.lastScorePercentage,
    this.attempted = true,
    required this.questions,
  });
}

class AssessmentResult {
  final int score;
  final int total;
  final int percentage;
  final List<String> strongAreas;
  final List<String> needsPractice;
  final String aiRecommendation;

  const AssessmentResult({
    required this.score,
    required this.total,
    required this.percentage,
    required this.strongAreas,
    required this.needsPractice,
    required this.aiRecommendation,
  });
}

class Recommendation {
  final String title;
  final String subjectName;
  final String description;
  final String actionLabel;

  const Recommendation({
    required this.title,
    required this.subjectName,
    required this.description,
    required this.actionLabel,
  });
}

class ChatMessage {
  final String id;
  final String sender; // 'user' or 'ai'
  final String message;
  final DateTime timestamp;
  final String explanationMode; // 'simple', 'real-world', 'technical'
  final String topic;
  final List<String> suggestedFollowups;
  final QuizData? quiz;
  final String? selectedQuizAnswerKey;
  final bool? isQuizAnswerCorrect;
  final String? quizFeedbackExplanation;

  ChatMessage({
    required this.id,
    required this.sender,
    required this.message,
    required this.timestamp,
    this.explanationMode = 'simple',
    this.topic = 'Computer Networks',
    this.suggestedFollowups = const [],
    this.quiz,
    this.selectedQuizAnswerKey,
    this.isQuizAnswerCorrect,
    this.quizFeedbackExplanation,
  });

  ChatMessage copyWith({
    String? selectedQuizAnswerKey,
    bool? isQuizAnswerCorrect,
    String? quizFeedbackExplanation,
  }) {
    return ChatMessage(
      id: id,
      sender: sender,
      message: message,
      timestamp: timestamp,
      explanationMode: explanationMode,
      topic: topic,
      suggestedFollowups: suggestedFollowups,
      quiz: quiz,
      selectedQuizAnswerKey: selectedQuizAnswerKey ?? this.selectedQuizAnswerKey,
      isQuizAnswerCorrect: isQuizAnswerCorrect ?? this.isQuizAnswerCorrect,
      quizFeedbackExplanation: quizFeedbackExplanation ?? this.quizFeedbackExplanation,
    );
  }
}
