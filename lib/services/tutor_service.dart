import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/constants/api_config.dart';
import '../data/mock/mock_data_service.dart';
import '../models/student_model.dart';
import 'learning_service.dart';

class TutorService {
  final String conversationId;

  TutorService({this.conversationId = 'default_conv'});

  Future<ChatMessage> sendQuestion({
    required String message,
    required String mode,
    String? action,
  }) async {
    final url = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.tutorChatEndpoint}');

    final payload = jsonEncode({
      'message': message,
      'explanation_mode': mode,
      'action': action,
      'conversation_id': conversationId,
      'student_context': {
        'student_name': MockDataService.currentStudent.name,
        'degree': MockDataService.currentStudent.degree,
        'current_subject': 'Computer Networks',
        'current_topic': 'TCP',
        'weak_topic': LearningService.currentProfile.weakTopics.isNotEmpty
            ? LearningService.currentProfile.weakTopics.first
            : 'TCP connection termination',
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

        QuizData? quiz;
        if (data['quiz'] != null) {
          quiz = QuizData.fromJson(data['quiz']);
        }

        List<String> followups = [];
        if (data['suggested_followups'] != null) {
          followups = List<String>.from(data['suggested_followups']);
        }

        return ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          sender: 'ai',
          message: data['answer'] ?? '',
          timestamp: DateTime.now(),
          explanationMode: data['explanation_mode'] ?? mode,
          topic: data['topic'] ?? 'Computer Networks',
          suggestedFollowups: followups,
          quiz: quiz,
        );
      } else {
        return _fallbackResponse(message, mode, action);
      }
    } catch (e) {
      // Offline fallback strategy for zero-downtime resilience
      return _fallbackResponse(message, mode, action);
    }
  }

  Future<Map<String, dynamic>> checkQuizAnswer({
    required String quizId,
    required String selectedKey,
    required String correctKey,
    required String explanation,
  }) async {
    final url = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.quizCheckEndpoint}');

    final payload = jsonEncode({
      'quiz_id': quizId,
      'selected_key': selectedKey,
      'correct_key': correctKey,
      'explanation': explanation,
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
        return jsonDecode(response.body);
      }
    } catch (_) {}

    // Offline fallback evaluation
    final isCorrect = selectedKey.trim().toUpperCase() == correctKey.trim().toUpperCase();
    return {
      'is_correct': isCorrect,
      'title': isCorrect ? 'Correct! 🎉' : 'Not quite 💡',
      'feedback': isCorrect
          ? 'Option $selectedKey is correct!'
          : 'Option $selectedKey is incorrect. The correct answer is Option $correctKey.',
      'explanation': explanation,
    };
  }

  Future<void> resetConversation() async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.resetChatEndpoint}?conversation_id=$conversationId');
      await http.post(url).timeout(const Duration(seconds: 3));
    } catch (_) {}
  }

  ChatMessage _fallbackResponse(String message, String mode, String? action) {
    final lower = message.toLowerCase();

    if (action == 'quiz_me') {
      return ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        sender: 'ai',
        message: '### Quick Check Quiz 🎯\nTest your understanding of the TCP connection process below:',
        timestamp: DateTime.now(),
        explanationMode: 'quiz',
        topic: 'TCP / IP Protocols',
        suggestedFollowups: const ['Explain SYN-ACK in detail', 'Practice another question'],
        quiz: const QuizData(
          id: 'quiz_tcp_1',
          question: 'Which message is sent by the server after receiving the initial SYN from the client?',
          options: [
            QuestionOption(key: 'A', text: 'SYN'),
            QuestionOption(key: 'B', text: 'SYN-ACK'),
            QuestionOption(key: 'C', text: 'ACK'),
            QuestionOption(key: 'D', text: 'FIN'),
          ],
          correctKey: 'B',
          explanation: 'The server responds with SYN-ACK to acknowledge the client\'s SYN and initiate bidirectional synchronization.',
        ),
      );
    }

    if (action == 'practice_topic') {
      return ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        sender: 'ai',
        message: '### Practice Problem 📝\nHere is a practice question tailored to your current topic:',
        timestamp: DateTime.now(),
        explanationMode: 'practice',
        topic: 'TCP / IP Protocols',
        suggestedFollowups: const ['Show solution breakdown', 'Quiz me on another topic'],
        quiz: const QuizData(
          id: 'practice_tcp_2',
          question: 'Why is TCP referred to as a connection-oriented protocol?',
          options: [
            QuestionOption(key: 'A', text: 'It transmits data without verifying receiver readiness'),
            QuestionOption(key: 'B', text: 'It establishes a handshake and sequence tracking before sending data'),
            QuestionOption(key: 'C', text: 'It uses broadcast packets exclusively'),
            QuestionOption(key: 'D', text: 'It runs on physical hardware only'),
          ],
          correctKey: 'B',
          explanation: 'TCP establishes sequence tracking and a 3-way handshake prior to payload transfer to guarantee reliable delivery.',
        ),
      );
    }

    String answer;
    List<String> followups;

    if (lower.contains('tcp') || lower.contains('handshake')) {
      if (mode == 'simple') {
        answer = '### Explanation\nTCP uses a **three-way handshake** to make sure both devices are ready before sending data.\n\n### Step-by-Step\n1. Device A sends **SYN** ("Are you ready?").\n2. Device B replies **SYN-ACK** ("Yes, I am ready! Are you?").\n3. Device A sends **ACK** ("Great, let\'s start!").\n\n### Key Point\nThis prevents lost messages and confirms a clean connection!';
      } else if (mode == 'real-world') {
        answer = '### Real-World Analogy\nImagine calling a friend on a mobile phone:\n\n• **SYN**: You dial and say *"Hello, can you hear me?"*\n• **SYN-ACK**: Friend answers *"Yes, I hear you! Can you hear me?"*\n• **ACK**: You say *"Yes, perfectly!"*\n\nNow both of you know the line is clear!';
      } else {
        answer = '### Technical Specifications\nTCP Connection Establishment (RFC 793):\n\n1. **Client -> Server [SYN]**: Sends ISN (`seq = x`). Socket state: `SYN-SENT`.\n2. **Server -> Client [SYN-ACK]**: Server allocates buffers, acknowledges ISN (`ack = x + 1`), sends server ISN (`seq = y`). Socket state: `SYN-RECEIVED`.\n3. **Client -> Server [ACK]**: Client acknowledges server ISN (`ack = y + 1`). Both enter `ESTABLISHED` state.';
      }
      followups = const [
        'What happens if the third ACK is lost?',
        'Give me a real-world example',
        'Quiz me on TCP'
      ];
    } else {
      answer = '### Explanation\nLearnSync AI analyzed your question.\n\n### Key Concept\nIn computer science, mastering foundational structures allows you to design efficient, reliable systems.\n\n### Next Step\nUse the buttons below to switch explanation depth or test your knowledge!';
      followups = const [
        'Explain this simply',
        'Give me a real-world example',
        'Quiz me on this topic'
      ];
    }

    return ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      sender: 'ai',
      message: answer,
      timestamp: DateTime.now(),
      explanationMode: mode,
      topic: 'Computer Networks',
      suggestedFollowups: followups,
    );
  }
}
