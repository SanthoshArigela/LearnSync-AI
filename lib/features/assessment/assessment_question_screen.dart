import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../models/student_model.dart';
import '../../services/assessment_service.dart';

class AssessmentQuestionScreen extends StatefulWidget {
  final String subject;
  final String topic;
  final String difficulty;
  final List<Question> questions;
  final VoidCallback onCancel;
  final Function(AssessmentResult result, List<Map<String, dynamic>> submissions, List<String> adaptivePath) onSubmitAssessment;

  const AssessmentQuestionScreen({
    super.key,
    required this.subject,
    required this.topic,
    required this.difficulty,
    required this.questions,
    required this.onCancel,
    required this.onSubmitAssessment,
  });

  @override
  State<AssessmentQuestionScreen> createState() =>
      _AssessmentQuestionScreenState();
}

class _AssessmentQuestionScreenState extends State<AssessmentQuestionScreen> {
  int _currentIndex = 0;
  final Map<int, String> _selectedAnswers = {};
  final List<String> _adaptivePath = [];
  String _currentDifficulty = 'Medium';
  bool _isEvaluating = false;

  final AssessmentService _service = AssessmentService();

  @override
  void initState() {
    super.initState();
    _currentDifficulty = widget.difficulty == 'Adaptive' ? 'Medium' : widget.difficulty;
  }

  void _onNextOrSubmit() async {
    final currentQ = widget.questions[_currentIndex];
    final selectedKey = _selectedAnswers[_currentIndex] ?? 'A';
    final isCorrect = selectedKey.toUpperCase() == currentQ.correctOptionKey.toUpperCase();

    // Record Adaptive Path step
    if (widget.difficulty == 'Adaptive') {
      _adaptivePath.add('$_currentDifficulty (${isCorrect ? "✓" : "✗"})');

      // Adaptive Rule: Correct -> increase difficulty; Incorrect -> decrease difficulty
      if (isCorrect) {
        _currentDifficulty = 'Hard';
      } else {
        _currentDifficulty = 'Medium';
      }
    }

    if (_currentIndex < widget.questions.length - 1) {
      setState(() {
        _currentIndex++;
      });
    } else {
      // Evaluate Assessment
      setState(() {
        _isEvaluating = true;
      });

      List<Map<String, dynamic>> submissions = [];
      for (int i = 0; i < widget.questions.length; i++) {
        final q = widget.questions[i];
        submissions.add({
          'question_id': q.id,
          'question_text': q.text,
          'selected_key': _selectedAnswers[i] ?? 'A',
          'correct_key': q.correctOptionKey,
          'topic': widget.topic,
          'subtopic': widget.topic,
          'explanation': q.explanation,
        });
      }

      final result = await _service.evaluateAssessment(
        assessmentId: 'ass_${DateTime.now().millisecondsSinceEpoch}',
        subject: widget.subject,
        topic: widget.topic,
        difficulty: widget.difficulty,
        submissions: submissions,
        adaptivePath: _adaptivePath,
      );

      if (!mounted) return;

      widget.onSubmitAssessment(result, submissions, _adaptivePath);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isEvaluating) {
      return Scaffold(
        body: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                CircularProgressIndicator(color: AppTheme.primary),
                SizedBox(height: 16),
                Text(
                  'LearnSync AI is evaluating your answers...',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 4),
                Text(
                  'Calculating score → Identifying strong & weak areas',
                  style: TextStyle(fontSize: 12, color: AppTheme.textSecondaryLight),
                ),
              ],
            ),
          ),
        ),
      );
    }

    final currentQ = widget.questions[_currentIndex];
    final progress = (_currentIndex + 1) / widget.questions.length;
    final isLast = _currentIndex == widget.questions.length - 1;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.close_rounded),
          onPressed: widget.onCancel,
        ),
        title: Text(widget.subject),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Progress Header & Adaptive Badge
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Question ${_currentIndex + 1} of ${widget.questions.length}',
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primary,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppTheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      widget.difficulty == 'Adaptive'
                          ? 'Adaptive: $_currentDifficulty'
                          : widget.difficulty,
                      style: const TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.primary,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              ClipRRect(
                borderRadius: BorderRadius.circular(6),
                child: LinearProgressIndicator(
                  value: progress,
                  minHeight: 8,
                  backgroundColor: AppTheme.cardBorder,
                  valueColor: const AlwaysStoppedAnimation<Color>(AppTheme.primary),
                ),
              ),
              const SizedBox(height: 20),

              // Question Text Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppTheme.cardBorder),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.02),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Text(
                  currentQ.text,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    height: 1.4,
                    color: AppTheme.textPrimaryLight,
                  ),
                ),
              ),
              const SizedBox(height: 20),

              const Text(
                'Select your answer:',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textSecondaryLight,
                ),
              ),
              const SizedBox(height: 12),

              // Options List
              Expanded(
                child: ListView.builder(
                  itemCount: currentQ.options.length,
                  itemBuilder: (context, optIndex) {
                    final opt = currentQ.options[optIndex];
                    final isSelected = _selectedAnswers[_currentIndex] == opt.key;

                    return Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: InkWell(
                        onTap: () {
                          setState(() {
                            _selectedAnswers[_currentIndex] = opt.key;
                          });
                        },
                        borderRadius: BorderRadius.circular(16),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 16),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? AppTheme.primary.withOpacity(0.08)
                                : Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: isSelected
                                  ? AppTheme.primary
                                  : AppTheme.cardBorder,
                              width: isSelected ? 2 : 1,
                            ),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 34,
                                height: 34,
                                decoration: BoxDecoration(
                                  color: isSelected
                                      ? AppTheme.primary
                                      : AppTheme.backgroundLight,
                                  shape: BoxShape.circle,
                                  border: Border.all(
                                    color: isSelected
                                        ? AppTheme.primary
                                        : AppTheme.cardBorder,
                                  ),
                                ),
                                child: Center(
                                  child: Text(
                                    opt.key,
                                    style: TextStyle(
                                      color: isSelected
                                          ? Colors.white
                                          : AppTheme.textPrimaryLight,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 14,
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Text(
                                  opt.text,
                                  style: TextStyle(
                                    fontSize: 15,
                                    fontWeight: isSelected
                                        ? FontWeight.bold
                                        : FontWeight.normal,
                                    color: isSelected
                                        ? AppTheme.primaryDark
                                        : AppTheme.textPrimaryLight,
                                  ),
                                ),
                              ),
                              if (isSelected)
                                const Icon(Icons.check_circle_rounded,
                                    color: AppTheme.primary, size: 22),
                            ],
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),

              // Bottom Navigation Buttons
              Row(
                children: [
                  if (_currentIndex > 0)
                    Expanded(
                      child: SecondaryButton(
                        label: 'Previous',
                        onPressed: () {
                          setState(() {
                            _currentIndex--;
                          });
                        },
                      ),
                    ),
                  if (_currentIndex > 0) const SizedBox(width: 12),
                  Expanded(
                    child: PrimaryButton(
                      label: isLast ? 'Submit Assessment' : 'Next',
                      icon: isLast ? Icons.check_rounded : Icons.arrow_forward_rounded,
                      onPressed: _onNextOrSubmit,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
