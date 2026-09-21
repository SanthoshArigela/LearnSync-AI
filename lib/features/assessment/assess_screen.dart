import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../data/mock/mock_data_service.dart';
import '../../models/student_model.dart';

class AssessScreen extends StatelessWidget {
  final VoidCallback onOpenConfig;
  final Function(Assessment assessment) onStartDirectAssessment;

  const AssessScreen({
    super.key,
    required this.onOpenConfig,
    required this.onStartDirectAssessment,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text('Quick Assessments', style: TextStyle(fontWeight: FontWeight.bold)),
            Text(
              'Test your understanding and discover what to improve.',
              style: TextStyle(fontSize: 12, color: AppTheme.textSecondaryLight),
            ),
          ],
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Custom AI Assessment Config Banner
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF4F46E5), Color(0xFF6366F1)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.auto_awesome, color: Colors.white, size: 28),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text(
                            'AI Adaptive Assessment',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                          SizedBox(height: 2),
                          Text(
                            'Custom subject, topic & adaptive difficulty mode.',
                            style: TextStyle(color: Colors.white87, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppTheme.primaryDark,
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                      ),
                      onPressed: onOpenConfig,
                      child: const Text('Configure', style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 18),

              const Text(
                'Available Assessments',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),

              Expanded(
                child: ListView.builder(
                  itemCount: MockDataService.assessments.length,
                  itemBuilder: (context, index) {
                    final item = MockDataService.assessments[index];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 14),
                      child: _buildAssessmentCard(context, item),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAssessmentCard(BuildContext context, Assessment assessment) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.cardBorder),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                assessment.subjectName,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: assessment.attempted
                      ? AppTheme.primary.withOpacity(0.1)
                      : Colors.orange.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  assessment.attempted
                      ? 'Last Score: ${assessment.lastScorePercentage}%'
                      : 'Not Attempted',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: assessment.attempted ? AppTheme.primary : Colors.orange[800],
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Icon(Icons.quiz_outlined, size: 16, color: AppTheme.textSecondaryLight),
              const SizedBox(width: 4),
              Text(
                '${assessment.totalQuestions} Questions',
                style: const TextStyle(fontSize: 13, color: AppTheme.textSecondaryLight),
              ),
              const SizedBox(width: 16),
              Icon(Icons.speed_rounded, size: 16, color: AppTheme.textSecondaryLight),
              const SizedBox(width: 4),
              Text(
                assessment.difficulty,
                style: const TextStyle(fontSize: 13, color: AppTheme.textSecondaryLight),
              ),
            ],
          ),
          const SizedBox(height: 16),
          PrimaryButton(
            label: 'Start Assessment',
            icon: Icons.play_arrow_rounded,
            onPressed: () => onStartDirectAssessment(assessment),
          ),
        ],
      ),
    );
  }
}
