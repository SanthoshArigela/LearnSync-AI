import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../data/mock/mock_data_service.dart';
import '../../models/student_model.dart';
import '../../services/tutor_service.dart';
import '../../services/local_ai_service.dart';

class AiTutorScreen extends StatefulWidget {
  final VoidCallback? onOpenCamera;
  final VoidCallback? onOpenVoice;
  final String? initialQuery;

  const AiTutorScreen({
    super.key,
    this.onOpenCamera,
    this.onOpenVoice,
    this.initialQuery,
  });

  @override
  State<AiTutorScreen> createState() => _AiTutorScreenState();
}

class _AiTutorScreenState extends State<AiTutorScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  late TutorService _tutorService;
  late LocalAiService _localAiService;
  late List<ChatMessage> _messages;

  String _currentMode = 'simple'; // 'simple', 'real-world', 'technical'
  bool _isThinking = false;
  String? _errorMessage;
  LocalAiCapability? _aiCapability;

  @override
  void initState() {
    super.initState();
    _tutorService = TutorService(conversationId: 'session_${DateTime.now().millisecondsSinceEpoch}');
    _localAiService = LocalAiService();
    _refreshAiStatus();

    _messages = [
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
            'TCP uses a three-way handshake to establish a reliable connection between two devices before data is exchanged.\n\n1. **SYN**: Client asks to sync.\n2. **SYN-ACK**: Server acknowledges and syncs back.\n3. **ACK**: Client confirms.',
        timestamp: DateTime.now().subtract(const Duration(minutes: 4)),
        explanationMode: 'simple',
        topic: 'Computer Networks → TCP',
        suggestedFollowups: const [
          'Explain SYN and ACK in detail',
          'Give me a real-world example',
          'Quiz me on TCP',
        ],
      ),
    ];

    if (widget.initialQuery != null && widget.initialQuery!.isNotEmpty) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _handleSubmitted(widget.initialQuery!);
      });
    }
  }

  void _refreshAiStatus() async {
    final cap = await _localAiService.fetchAiStatus();
    if (mounted) {
      setState(() {
        _aiCapability = cap;
      });
    }
  }

  void _handleSubmitted(String text, {String? action, String? overrideMode}) async {
    if (text.trim().isEmpty && action == null) return;

    final targetMode = overrideMode ?? _currentMode;

    // Add user message if text is present
    if (text.trim().isNotEmpty) {
      final userMsg = ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        sender: 'user',
        message: text,
        timestamp: DateTime.now(),
      );
      setState(() {
        _messages.add(userMsg);
        _textController.clear();
        _isThinking = true;
        _errorMessage = null;
      });
      _scrollToBottom();
    } else {
      setState(() {
        _isThinking = true;
        _errorMessage = null;
      });
    }

    try {
      final aiResponseMsg = await _tutorService.sendQuestion(
        message: text.isEmpty ? "Explain topic" : text,
        mode: targetMode,
        action: action,
      );

      if (!mounted) return;

      setState(() {
        _messages.add(aiResponseMsg);
        _isThinking = false;
        _currentMode = targetMode;
      });
      _refreshAiStatus();
      _scrollToBottom();
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isThinking = false;
        _errorMessage = 'I couldn\'t reach the AI right now. Please try again.';
      });
    }
  }

  void _switchExplanationMode(String mode) {
    if (_currentMode == mode) return;
    setState(() {
      _currentMode = mode;
    });

    final lastUserMsg = _messages.lastWhere(
      (m) => m.sender == 'user',
      orElse: () => ChatMessage(
        id: '0',
        sender: 'user',
        message: 'Why does TCP use a three-way handshake?',
        timestamp: DateTime.now(),
      ),
    );

    _handleSubmitted('Explain using $mode explanation.', overrideMode: mode);
  }

  void _handleQuizOptionSelect(ChatMessage msg, QuizData quiz, String selectedKey) async {
    final res = await _tutorService.checkQuizAnswer(
      quizId: quiz.id,
      selectedKey: selectedKey,
      correctKey: quiz.correctKey,
      explanation: quiz.explanation,
    );

    if (!mounted) return;

    final index = _messages.indexWhere((m) => m.id == msg.id);
    if (index != -1) {
      setState(() {
        _messages[index] = msg.copyWith(
          selectedQuizAnswerKey: selectedKey,
          isQuizAnswerCorrect: res['is_correct'] ?? false,
          quizFeedbackExplanation: '${res['title']}\n${res['feedback']}\n\n${res['explanation']}',
        );
      });
    }
  }

  void _resetNewChat() {
    setState(() {
      _tutorService.resetConversation();
      _messages = [
        ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          sender: 'ai',
          message: 'Hello Santhosh! 👋 What concept or subject would you like to explore today?',
          timestamp: DateTime.now(),
          suggestedFollowups: const [
            'Why does TCP use a three-way handshake?',
            'What is the OSI model?',
            'Quiz me on DBMS',
          ],
        ),
      ];
      _errorMessage = null;
    });
    _refreshAiStatus();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Widget _buildStatusBadge() {
    final provider = _aiCapability?.activeProvider ?? 'gemini';
    final runtime = _aiCapability?.localRuntime ?? 'Local CPU Fallback';
    final isNpu = _aiCapability?.hardwareAcceleration ?? false;

    Color badgeBg;
    Color borderBg;
    Color textColor;
    String badgeText;

    if (provider == 'local') {
      badgeBg = const Color(0xFFD1FAE5);
      borderBg = const Color(0xFF6EE7B7);
      textColor = const Color(0xFF065F46);
      badgeText = '● Local AI Engine';
    } else if (provider == 'gemini') {
      badgeBg = const Color(0xFFE0F2FE);
      borderBg = const Color(0xFF7DD3FC);
      textColor = const Color(0xFF0369A1);
      badgeText = '● Cloud AI (Gemini)';
    } else {
      badgeBg = const Color(0xFFFEF3C7);
      borderBg = const Color(0xFFFCD34D);
      textColor = const Color(0xFF92400E);
      badgeText = '● Offline AI (Fallback Mode)';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: badgeBg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: borderBg),
      ),
      child: Text(
        badgeText,
        style: TextStyle(fontSize: 9.5, fontWeight: FontWeight.bold, color: textColor),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.auto_awesome, color: AppTheme.primary, size: 20),
                const SizedBox(width: 8),
                const Text('LearnSync AI', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(width: 8),
                Expanded(child: SingleChildScrollView(scrollDirection: Axis.horizontal, child: _buildStatusBadge())),
              ],
            ),
            const Text(
              'Your Personal Learning Assistant',
              style: TextStyle(fontSize: 12, color: AppTheme.textSecondaryLight),
            ),
          ],
        ),
        actions: [
          TextButton.icon(
            icon: const Icon(Icons.add_comment_outlined, size: 18, color: AppTheme.primary),
            label: const Text('New Chat', style: TextStyle(color: AppTheme.primary, fontWeight: FontWeight.bold)),
            onPressed: _resetNewChat,
          ),
        ],
      ),

      body: SafeArea(
        child: Column(
          children: [
            // Mode Selector Bar
            _buildModeSelectorBar(),

            // Chat Message Trajectory
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(16),
                itemCount: _messages.length + (_isThinking ? 1 : 0) + (_errorMessage != null ? 1 : 0),
                itemBuilder: (context, index) {
                  if (index == _messages.length && _isThinking) {
                    return _buildThinkingIndicator();
                  }

                  if (index == _messages.length + (_isThinking ? 1 : 0) && _errorMessage != null) {
                    return _buildErrorMessage();
                  }

                  final msg = _messages[index];
                  final isUser = msg.sender == 'user';

                  return Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: Column(
                      crossAxisAlignment:
                          isUser ? CrossAlignment.end : CrossAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment:
                              isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
                          crossAxisAlignment: CrossAlignment.start,
                          children: [
                            if (!isUser) ...[
                              CircleAvatar(
                                radius: 16,
                                backgroundColor: AppTheme.primary,
                                child: const Icon(Icons.auto_awesome,
                                    size: 16, color: Colors.white),
                              ),
                              const SizedBox(width: 8),
                            ],
                            Flexible(
                              child: Container(
                                padding: const EdgeInsets.all(14),
                                decoration: BoxDecoration(
                                  color: isUser
                                      ? AppTheme.primary
                                      : Colors.white,
                                  borderRadius: BorderRadius.only(
                                    topLeft: const Radius.circular(18),
                                    topRight: const Radius.circular(18),
                                    bottomLeft: Radius.circular(isUser ? 18 : 4),
                                    bottomRight: Radius.circular(isUser ? 4 : 18),
                                  ),
                                  border: isUser
                                      ? null
                                      : Border.all(color: AppTheme.cardBorder),
                                  boxShadow: [
                                    BoxShadow(
                                      color: Colors.black.withOpacity(0.02),
                                      blurRadius: 6,
                                      offset: const Offset(0, 2),
                                    ),
                                  ],
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAlignment.start,
                                  children: [
                                    if (!isUser) ...[
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            msg.topic,
                                            style: const TextStyle(
                                              fontSize: 11,
                                              fontWeight: FontWeight.bold,
                                              color: AppTheme.primary,
                                            ),
                                          ),
                                          Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                            decoration: BoxDecoration(
                                              color: AppTheme.primary.withOpacity(0.1),
                                              borderRadius: BorderRadius.circular(8),
                                            ),
                                            child: Text(
                                              msg.explanationMode.toUpperCase(),
                                              style: const TextStyle(
                                                fontSize: 9,
                                                fontWeight: FontWeight.bold,
                                                color: AppTheme.primary,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 6),
                                    ],
                                    Text(
                                      msg.message,
                                      style: TextStyle(
                                        color: isUser
                                            ? Colors.white
                                            : AppTheme.textPrimaryLight,
                                        fontSize: 14.5,
                                        height: 1.4,
                                      ),
                                    ),

                                    // Render Quiz Card if present
                                    if (!isUser && msg.quiz != null) ...[
                                      const SizedBox(height: 12),
                                      _buildQuizCard(msg, msg.quiz!),
                                    ],
                                  ],
                                ),
                              ),
                            ),
                            if (isUser) ...[
                              const SizedBox(width: 8),
                              const CircleAvatar(
                                radius: 16,
                                backgroundColor: AppTheme.secondary,
                                child: Icon(Icons.person, size: 16, color: Colors.white),
                              ),
                            ],
                          ],
                        ),

                        // Suggested Follow-up Chips
                        if (!isUser && msg.suggestedFollowups.isNotEmpty) ...[
                          const SizedBox(height: 10),
                          Padding(
                            padding: const EdgeInsets.only(left: 40),
                            child: Wrap(
                              spacing: 6,
                              runSpacing: 6,
                              children: msg.suggestedFollowups.map((fUp) {
                                return ActionChip(
                                  backgroundColor: const Color(0xFFEEF2FF),
                                  side: const BorderSide(color: Color(0xFFC7D2FE)),
                                  avatar: const Icon(Icons.arrow_outward_rounded, size: 14, color: AppTheme.primary),
                                  label: Text(
                                    fUp,
                                    style: const TextStyle(
                                      color: AppTheme.primary,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 12,
                                    ),
                                  ),
                                  onPressed: () => _handleSubmitted(fUp),
                                );
                              }).toList(),
                            ),
                          ),
                        ],
                      ],
                    ),
                  );
                },
              ),
            ),

            // Quick Actions Toolbar
            _buildQuickActionsToolbar(),

            // Chat Input Bar
            _buildInputBar(),
          ],
        ),
      ),
    );
  }

  Widget _buildModeSelectorBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      color: Colors.white,
      child: Row(
        children: [
          const Text(
            'Mode:',
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textSecondaryLight),
          ),
          const SizedBox(width: 10),
          _buildModeChip('simple', 'Simple'),
          const SizedBox(width: 6),
          _buildModeChip('real-world', 'Real-world'),
          const SizedBox(width: 6),
          _buildModeChip('technical', 'Technical'),
        ],
      ),
    );
  }

  Widget _buildModeChip(String key, String label) {
    final isSelected = _currentMode == key;
    return InkWell(
      onTap: () => _switchExplanationMode(key),
      borderRadius: BorderRadius.circular(16),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.primary : AppTheme.backgroundLight,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: isSelected ? AppTheme.primary : AppTheme.cardBorder),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: isSelected ? Colors.white : AppTheme.textSecondaryLight,
          ),
        ),
      ),
    );
  }

  Widget _buildQuickActionsToolbar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      color: AppTheme.backgroundLight,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            _buildActionButtonChip(
              icon: Icons.quiz_outlined,
              label: 'Quiz me',
              onTap: () => _handleSubmitted('Quiz me on this topic', action: 'quiz_me'),
            ),
            const SizedBox(width: 6),
            _buildActionButtonChip(
              icon: Icons.psychology_outlined,
              label: 'Practice this topic',
              onTap: () => _handleSubmitted('Generate a practice question', action: 'practice_topic'),
            ),
            const SizedBox(width: 6),
            _buildActionButtonChip(
              icon: Icons.lightbulb_outline_rounded,
              label: 'Give me an example',
              onTap: () => _switchExplanationMode('real-world'),
            ),
            const SizedBox(width: 6),
            _buildActionButtonChip(
              icon: Icons.summarize_outlined,
              label: 'Summarize',
              onTap: () => _handleSubmitted('Summarize this concept in 3 key points'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButtonChip({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return OutlinedButton.icon(
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        side: const BorderSide(color: AppTheme.cardBorder),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        backgroundColor: Colors.white,
      ),
      icon: Icon(icon, size: 14, color: AppTheme.primary),
      label: Text(label, style: const TextStyle(fontSize: 11, color: AppTheme.textPrimaryLight, fontWeight: FontWeight.w600)),
      onPressed: onTap,
    );
  }

  Widget _buildQuizCard(ChatMessage msg, QuizData quiz) {
    final hasAnswered = msg.selectedQuizAnswerKey != null;

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppTheme.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            quiz.question,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13.5),
          ),
          const SizedBox(height: 10),
          ...quiz.options.map((opt) {
            final isThisSelected = msg.selectedQuizAnswerKey == opt.key;
            Color optColor = Colors.white;
            Color borderColor = AppTheme.cardBorder;

            if (hasAnswered && isThisSelected) {
              final isCorrect = msg.isQuizAnswerCorrect ?? false;
              optColor = isCorrect ? AppTheme.success.withOpacity(0.1) : Colors.red.withOpacity(0.1);
              borderColor = isCorrect ? AppTheme.success : Colors.red;
            }

            return Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: InkWell(
                onTap: hasAnswered ? null : () => _handleQuizOptionSelect(msg, quiz, opt.key),
                borderRadius: BorderRadius.circular(10),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: optColor,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: borderColor),
                  ),
                  child: Row(
                    children: [
                      Text(
                        '${opt.key}. ',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                      ),
                      Expanded(
                        child: Text(
                          opt.text,
                          style: const TextStyle(fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            );
          }),
          if (hasAnswered && msg.quizFeedbackExplanation != null) ...[
            const SizedBox(height: 8),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: (msg.isQuizAnswerCorrect ?? false)
                    ? AppTheme.success.withOpacity(0.12)
                    : Colors.orange.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                msg.quizFeedbackExplanation!,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: (msg.isQuizAnswerCorrect ?? false)
                      ? AppTheme.success
                      : Colors.orange[900],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildInputBar() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: Row(
        children: [
          if (widget.onOpenCamera != null)
            IconButton(
              icon: const Icon(Icons.camera_alt_outlined, color: AppTheme.primary),
              onPressed: widget.onOpenCamera,
            ),
          if (widget.onOpenVoice != null)
            IconButton(
              icon: const Icon(Icons.mic_none_rounded, color: AppTheme.primary),
              onPressed: widget.onOpenVoice,
            ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              decoration: BoxDecoration(
                color: AppTheme.backgroundLight,
                borderRadius: BorderRadius.circular(24),
                border: Border.all(color: AppTheme.cardBorder),
              ),
              child: TextField(
                controller: _textController,
                onSubmitted: (val) => _handleSubmitted(val),
                decoration: const InputDecoration(
                  hintText: 'Ask anything about your studies...',
                  hintStyle: TextStyle(fontSize: 13, color: AppTheme.textSecondaryLight),
                  border: InputBorder.none,
                ),
              ),
            ),
          ),
          const SizedBox(width: 8),
          Container(
            decoration: const BoxDecoration(
              color: AppTheme.primary,
              shape: BoxShape.circle,
            ),
            child: IconButton(
              icon: const Icon(Icons.send_rounded, color: Colors.white, size: 20),
              onPressed: () => _handleSubmitted(_textController.text),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildThinkingIndicator() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        children: [
          CircleAvatar(
            radius: 16,
            backgroundColor: AppTheme.primary,
            child: const Icon(Icons.auto_awesome, size: 16, color: Colors.white),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: AppTheme.cardBorder),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: const [
                SizedBox(
                  width: 14,
                  height: 14,
                  child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primary),
                ),
                SizedBox(width: 10),
                Text(
                  'LearnSync AI is thinking...',
                  style: TextStyle(
                    fontSize: 13,
                    color: AppTheme.textSecondaryLight,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorMessage() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.red.withOpacity(0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.red.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.error_outline_rounded, color: Colors.red, size: 20),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red, fontSize: 13),
              ),
            ),
            TextButton(
              onPressed: () {
                final last = _messages.lastWhere((m) => m.sender == 'user', orElse: () => _messages.last);
                _handleSubmitted(last.message);
              },
              child: const Text('Retry', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
            ),
          ],
        ),
      ),
    );
  }
}
