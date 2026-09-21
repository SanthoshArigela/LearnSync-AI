import '../../models/student_model.dart';

class MockDataService {
  static const Student currentStudent = Student(
    id: 'std_101',
    name: 'Santhosh',
    degree: 'B.Tech CSE',
  );

  static const Recommendation currentRecommendation = Recommendation(
    title: 'Revise OSI Model',
    subjectName: 'Computer Networks',
    description: 'You showed difficulty with Layers 3 and 4 in your recent practice.',
    actionLabel: 'Start Revision',
  );

  static const List<Subject> subjects = [
    Subject(
      id: 'sub_cn',
      title: 'Computer Networks',
      totalTopics: 10,
      progressPercentage: 82,
      iconName: 'wifi',
    ),
    Subject(
      id: 'sub_ds',
      title: 'Data Structures',
      totalTopics: 12,
      progressPercentage: 76,
      iconName: 'account_tree',
    ),
    Subject(
      id: 'sub_dbms',
      title: 'Database Management',
      totalTopics: 8,
      progressPercentage: 71,
      iconName: 'storage',
    ),
    Subject(
      id: 'sub_os',
      title: 'Operating Systems',
      totalTopics: 9,
      progressPercentage: 58,
      iconName: 'memory',
    ),
    Subject(
      id: 'sub_ml',
      title: 'Machine Learning',
      totalTopics: 11,
      progressPercentage: 64,
      iconName: 'psychology',
    ),
  ];

  static const List<Assessment> assessments = [
    Assessment(
      id: 'ass_cn',
      subjectName: 'Computer Networks',
      totalQuestions: 5,
      difficulty: 'Medium',
      lastScorePercentage: 80,
      attempted: true,
      questions: cnQuestions,
    ),
    Assessment(
      id: 'ass_ds',
      subjectName: 'Data Structures',
      totalQuestions: 5,
      difficulty: 'Easy',
      lastScorePercentage: 90,
      attempted: true,
      questions: dsQuestions,
    ),
    Assessment(
      id: 'ass_dbms',
      subjectName: 'DBMS',
      totalQuestions: 10,
      difficulty: 'Medium',
      lastScorePercentage: null,
      attempted: false,
      questions: dbmsQuestions,
    ),
  ];

  static const List<Question> cnQuestions = [
    Question(
      id: 'q1',
      text: 'Which protocol provides reliable, connection-oriented communication?',
      options: [
        QuestionOption(key: 'A', text: 'UDP'),
        QuestionOption(key: 'B', text: 'TCP'),
        QuestionOption(key: 'C', text: 'IP'),
        QuestionOption(key: 'D', text: 'ARP'),
      ],
      correctOptionKey: 'B',
      explanation: 'TCP (Transmission Control Protocol) establishes a reliable connection before transmitting data.',
    ),
    Question(
      id: 'q2',
      text: 'Which layer of the OSI model deals with logical IP addressing?',
      options: [
        QuestionOption(key: 'A', text: 'Data Link Layer'),
        QuestionOption(key: 'B', text: 'Network Layer'),
        QuestionOption(key: 'C', text: 'Transport Layer'),
        QuestionOption(key: 'D', text: 'Application Layer'),
      ],
      correctOptionKey: 'B',
      explanation: 'The Network Layer (Layer 3) handles IP addressing and routing across networks.',
    ),
    Question(
      id: 'q3',
      text: 'What is the primary function of Domain Name System (DNS)?',
      options: [
        QuestionOption(key: 'A', text: 'Encrypt packet data'),
        QuestionOption(key: 'B', text: 'Resolve domain names to IP addresses'),
        QuestionOption(key: 'C', text: 'Manage network hardware'),
        QuestionOption(key: 'D', text: 'Detect transmission errors'),
      ],
      correctOptionKey: 'B',
      explanation: 'DNS maps human-readable domain names (e.g. google.com) to machine IP addresses.',
    ),
    Question(
      id: 'q4',
      text: 'Which mechanism is used by TCP for flow control?',
      options: [
        QuestionOption(key: 'A', text: 'Sliding Window Protocol'),
        QuestionOption(key: 'B', text: 'Stop and Wait'),
        QuestionOption(key: 'C', text: 'Token Bucket'),
        QuestionOption(key: 'D', text: 'CSMA/CD'),
      ],
      correctOptionKey: 'A',
      explanation: 'TCP uses dynamic sliding window mechanisms to regulate sender transmission rates.',
    ),
    Question(
      id: 'q5',
      text: 'Which packet exchange occurs during TCP connection termination?',
      options: [
        QuestionOption(key: 'A', text: 'SYN - SYN-ACK - ACK'),
        QuestionOption(key: 'B', text: 'FIN - ACK - FIN - ACK'),
        QuestionOption(key: 'C', text: 'RST - ACK'),
        QuestionOption(key: 'D', text: 'PING - PONG'),
      ],
      correctOptionKey: 'B',
      explanation: 'TCP connection release requires a four-way handshake starting with FIN control segments.',
    ),
  ];

  static const List<Question> dsQuestions = [
    Question(
      id: 'q_ds1',
      text: 'Which data structure operates on a First In First Out (FIFO) basis?',
      options: [
        QuestionOption(key: 'A', text: 'Stack'),
        QuestionOption(key: 'B', text: 'Queue'),
        QuestionOption(key: 'C', text: 'Tree'),
        QuestionOption(key: 'D', text: 'Graph'),
      ],
      correctOptionKey: 'B',
      explanation: 'Queue follows FIFO ordering where the first inserted element is dequeued first.',
    ),
  ];

  static const List<Question> dbmsQuestions = [
    Question(
      id: 'q_db1',
      text: 'What does ACID stand for in DBMS transactions?',
      options: [
        QuestionOption(key: 'A', text: 'Atomicity, Consistency, Isolation, Durability'),
        QuestionOption(key: 'B', text: 'Array, Column, Index, Database'),
        QuestionOption(key: 'C', text: 'Access, Control, Interface, Data'),
        QuestionOption(key: 'D', text: 'Aggregation, Concurrency, Integrity, Deletion'),
      ],
      correctOptionKey: 'A',
      explanation: 'ACID guarantees reliability in database transactions.',
    ),
  ];

  static AssessmentResult getSampleResult() {
    return const AssessmentResult(
      score: 4,
      total: 5,
      percentage: 80,
      strongAreas: ['TCP basics', 'DNS'],
      needsPractice: ['TCP connection termination'],
      aiRecommendation:
          'You may need more practice with TCP connection termination. Spend 10 minutes reviewing this topic before your next assessment.',
    );
  }

  static List<ChatMessage> getInitialChatHistory() {
    return [
      ChatMessage(
        id: 'msg_1',
        sender: 'user',
        message: 'Why does TCP use a three-way handshake?',
        timestamp: DateTime.now().subtract(const Duration(minutes: 5)),
      ),
      ChatMessage(
        id: 'msg_2',
        sender: 'ai',
        message:
            'TCP uses a three-way handshake to establish a reliable connection between two devices before data is exchanged.',
        timestamp: DateTime.now().subtract(const Duration(minutes: 4)),
        explanationOptions: ['Simple', 'Real-world Example', 'Technical'],
      ),
    ];
  }

  static String getExplanationForOption(String option) {
    switch (option) {
      case 'Simple':
        return 'Think of it like calling a friend:\n1. You say "Hello!" (SYN)\n2. They say "Hello, I can hear you!" (SYN-ACK)\n3. You say "Great, let\'s talk!" (ACK)\nNow you both know the connection is clear!';
      case 'Real-world Example':
        return 'Imagine sending a registered letter:\nFirst, you send a notice asking if the recipient is ready (SYN). The recipient replies with a signed receipt (SYN-ACK). Finally, you confirm receipt (ACK) and start transmitting your package securely.';
      case 'Technical':
        return 'The TCP 3-way handshake synchronizes Sequence Numbers (ISN) and Acknowledgement numbers:\n• Client sends SYN (seq = x)\n• Server replies SYN-ACK (seq = y, ack = x + 1)\n• Client sends ACK (ack = y + 1)\nThis establishes bidirectional sequence tracking and socket buffers.';
      default:
        return 'TCP ensures reliable, ordered, and error-checked delivery of a stream of octets.';
    }
  }

  static String getMockAiResponse(String prompt) {
    final lower = prompt.toLowerCase();
    if (lower.contains('tcp') || lower.contains('handshake') || lower.contains('udp')) {
      return 'TCP (Transmission Control Protocol) is connection-oriented and guarantees packet delivery, whereas UDP (User Datagram Protocol) is connectionless and prioritizes speed over delivery verification.';
    } else if (lower.contains('osi') || lower.contains('layer')) {
      return 'The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application. Layers 3 (Network) and 4 (Transport) manage IP routing and TCP/UDP ports.';
    } else if (lower.contains('2x') || lower.contains('equation') || lower.contains('math')) {
      return 'To solve 2x + 5 = 15:\nStep 1: Subtract 5 from both sides => 2x = 10\nStep 2: Divide both sides by 2 => x = 5.';
    } else {
      return 'Great question! LearnSync AI analyzes your subject context to provide personalized breakdowns. Let\'s explore this concept step-by-step.';
    }
  }
}
