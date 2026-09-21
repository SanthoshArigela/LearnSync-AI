import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../models/student_model.dart';

class AssessmentResultScreen extends StatelessWidget {
  final AssessmentResult result;
  final List<Map<String, dynamic>>? submissions;
  final List<String>? adaptivePath;
  final VoidCallback onBackToAssessments;
  final Function(String weakTopic) onPracticeWeakTopic;
  final Function(Map<String, dynamic> mistake) onUnderstandMistake;

  const AssessmentResultScreen({
    super.key,
    required this.result,
    this.submissions,
    this.adaptivePath,
    required this.onBackToAssessments,
    required this.onPracticeWeakTopic,
    required this.onUnderstandMistake,
  });

  @override
  Widget build(BuildContext context) {
    final weakTopic = result.needsPractice.isNotEmpty
        ? result.needsPractice.first
        : 'TCP connection termination';

    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text('Assessment Result'),
        actions: [
          IconButton(
            icon: const Icon(Icons.close_rounded),
            onPressed: onBackToAssessments,
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 10),
              const Text(
                'Assessment Complete 🎉',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.extrabold,
                  color: AppTheme.textPrimaryLight,
                ),
              ),
              const SizedBox(height: 18),

              // Score Circle Display
              Container(
                width: 140,
                height: 140,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppTheme.primary.withOpacity(0.1),
                  border: Border.all(color: AppTheme.primary, width: 4),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '${result.score} / ${result.total}',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.extrabold,
                        color: AppTheme.primaryDark,
                      ),
                    ),
                    Text(
                      '${result.percentage}% Score',
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.primary,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Adaptive Path Display
              if (adaptivePath != null && adaptivePath!.isNotEmpty) ...[
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppTheme.primary.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppTheme.primary.withOpacity(0.3)),
                  ),
                  child: Text(
                    'Adaptive Path: ${adaptivePath!.join(" → ")}',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primary,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // Strong Areas
              Align(
                alignment: Alignment.centerLeft,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.check_circle_outline_rounded,
                            color: AppTheme.success, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Strong Areas',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    ...result.strongAreas.map(
                      (area) => Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 14, vertical: 10),
                          decoration: BoxDecoration(
                            color: AppTheme.success.withOpacity(0.08),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                                color: AppTheme.success.withOpacity(0.3)),
                          ),
                          child: Text(
                            '✓  $area',
                            style: const TextStyle(
                              color: AppTheme.success,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Needs Practice
              Align(
                alignment: Alignment.centerLeft,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.warning_amber_rounded,
                            color: Colors.orange, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Needs Practice',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    ...result.needsPractice.map(
                      (area) => Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 14, vertical: 10),
                          decoration: BoxDecoration(
                            color: Colors.orange.withOpacity(0.08),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.orange.withOpacity(0.3)),
                          ),
                          child: Text(
                            '⚠  $area',
                            style: TextStyle(
                              color: Colors.orange[900],
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // LearnSync AI Recommendation Card
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: const Color(0xFFEEF2FF),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFC7D2FE)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.auto_awesome, color: AppTheme.primary),
                        SizedBox(width: 8),
                        Text(
                          'LearnSync AI Recommendation',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                            color: AppTheme.primaryDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      result.aiRecommendation,
                      style: const TextStyle(
                        fontSize: 13.5,
                        color: Color(0xFF4338CA),
                        height: 1.4,
                      ),
                    ),
                    const SizedBox(height: 16),
                    PrimaryButton(
                      label: 'Practice Weak Topic ($weakTopic)',
                      icon: Icons.psychology_rounded,
                      onPressed: () => onPracticeWeakTopic(weakTopic),
                      backgroundColor: AppTheme.primaryDark,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Understand My Mistake Button
              SecondaryButton(
                label: 'Understand My Mistake with AI Tutor',
                icon: Icons.help_outline_rounded,
                onPressed: () {
                  final mistake = (submissions != null && submissions!.isNotEmpty)
                      ? submissions!.first
                      : {
                          'question_text': 'Which message is sent during TCP connection termination?',
                          'selected_key': 'UDP',
                          'correct_key': 'FIN-ACK',
                          'explanation': 'TCP termination requires FIN-ACK segments.'
                        };
                  onUnderstandMistake(mistake);
                },
              ),
              const SizedBox(height: 12),
              TextButton(
                onPressed: onBackToAssessments,
                child: const Text(
                  'Back to Assessments',
                  style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.textSecondaryLight),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
