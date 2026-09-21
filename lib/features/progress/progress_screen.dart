import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../data/mock/mock_data_service.dart';
import '../../models/learning_models.dart';
import '../../services/assessment_service.dart';
import '../../services/learning_service.dart';

class ProgressScreen extends StatelessWidget {
  final VoidCallback onStartRevision;

  const ProgressScreen({
    super.key,
    required this.onStartRevision,
  });

  @override
  Widget build(BuildContext context) {
    final history = AssessmentService.history;
    final profile = LearningService.currentProfile;
    final overallPct = profile.overallMastery;
    final nba = profile.nextBestAction;

    final strongList = profile.strongTopics.isNotEmpty
        ? profile.strongTopics
        : ['TCP Basics', 'DNS'];
    final weakList = profile.weakTopics.isNotEmpty
        ? profile.weakTopics
        : ['TCP Connection Termination', 'Process Scheduling'];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Learning Progress'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Overall Progress Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF3B82F6), Color(0xFF6366F1)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF3B82F6).withOpacity(0.3),
                      blurRadius: 14,
                      offset: const Offset(0, 6),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: const [
                              Text(
                                'Overall Mastery',
                                style: TextStyle(
                                  color: Colors.white70,
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              SizedBox(width: 8),
                              Icon(Icons.trending_up_rounded, color: Colors.white, size: 18),
                              SizedBox(width: 4),
                              Text(
                                'Improving ↗',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(
                            '$overallPct%',
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 36,
                              fontWeight: FontWeight.extrabold,
                            ),
                          ),
                          const SizedBox(height: 6),
                          const Text(
                            'Great job! Your performance profile updates dynamically based on assessment scores.',
                            style: TextStyle(
                              color: Colors.white90,
                              fontSize: 12.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 16),
                    Container(
                      width: 72,
                      height: 72,
                      decoration: const BoxDecoration(
                        color: Colors.white24,
                        shape: BoxShape.circle,
                      ),
                      child: const Center(
                        child: Icon(Icons.analytics_rounded,
                            color: Colors.white, size: 38),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),

              // Strong Areas & Needs Attention Cards
              Row(
                children: [
                  // Strong Areas
                  Expanded(
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.08),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.green.withOpacity(0.3)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: const [
                              Icon(Icons.check_circle_rounded, color: Colors.green, size: 18),
                              SizedBox(width: 6),
                              Text(
                                'Strong Areas',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF14532D),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          ...strongList.take(2).map(
                                (item) => Padding(
                                  padding: const EdgeInsets.only(bottom: 4),
                                  child: Text(
                                    '• $item',
                                    style: const TextStyle(
                                      fontSize: 12.5,
                                      fontWeight: FontWeight.w600,
                                      color: Color(0xFF166534),
                                    ),
                                  ),
                                ),
                              ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  // Needs Attention
                  Expanded(
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: Colors.amber.withOpacity(0.08),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.amber.withOpacity(0.4)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: const [
                              Icon(Icons.warning_amber_rounded, color: Colors.amber, size: 18),
                              SizedBox(width: 6),
                              Text(
                                'Needs Attention',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF92400E),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          ...weakList.take(2).map(
                                (item) => Padding(
                                  padding: const EdgeInsets.only(bottom: 4),
                                  child: Text(
                                    '• $item',
                                    style: const TextStyle(
                                      fontSize: 12.5,
                                      fontWeight: FontWeight.w600,
                                      color: Color(0xFF78350F),
                                    ),
                                  ),
                                ),
                              ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 22),

              // Recommended Next Step Card (Sprint 5 Requirement 25)
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: Colors.amber.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.amber.withOpacity(0.4)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.star_rounded, color: Color(0xFFD97706), size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Recommended Next Step',
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF92400E),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      nba?.title ?? 'Revise TCP Connection Termination',
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textPrimaryLight,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      nba?.reason ??
                          'Your recent answers suggest that connection termination needs more practice.',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFF78350F),
                      ),
                    ),
                    const SizedBox(height: 14),
                    PrimaryButton(
                      label: nba?.action == 'practice' ? 'Start Practice' : 'Start Revision',
                      icon: Icons.refresh_rounded,
                      onPressed: onStartRevision,
                      backgroundColor: const Color(0xFFD97706),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Performance Breakdown by Subject
              const Text(
                'Subject Mastery Breakdown',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              ...(profile.subjects.isNotEmpty
                      ? profile.subjects.values
                      : MockDataService.subjects)
                  .map(
                (subj) {
                  final String title = subj is SubjectMastery ? subj.subject : (subj as dynamic).title;
                  final int mastery = subj is SubjectMastery ? subj.overallMastery : (subj as dynamic).progressPercentage;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppTheme.cardBorder),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                title,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 14.5,
                                ),
                              ),
                              Text(
                                '$mastery%',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: mastery < 60
                                      ? Colors.orange
                                      : AppTheme.primary,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(6),
                            child: LinearProgressIndicator(
                              value: mastery / 100.0,
                              minHeight: 8,
                              backgroundColor: AppTheme.cardBorder,
                              valueColor: AlwaysStoppedAnimation<Color>(
                                mastery < 60
                                    ? Colors.orange
                                    : AppTheme.primary,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 22),

              // Statistics Section
              const Text(
                'Overall Learning Statistics',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
                childAspectRatio: 2.2,
                children: [
                  const StatisticCard(
                    value: '42 hours',
                    label: 'Total Learning Time',
                    icon: Icons.access_time_filled_rounded,
                    iconColor: AppTheme.primary,
                  ),
                  const StatisticCard(
                    value: '128',
                    label: 'Questions Answered',
                    icon: Icons.chat_rounded,
                    iconColor: AppTheme.secondary,
                  ),
                  StatisticCard(
                    value: '${16 + history.length}',
                    label: 'Assessments Completed',
                    icon: Icons.assignment_turned_in_rounded,
                    iconColor: AppTheme.accentPurple,
                  ),
                  StatisticCard(
                    value: '$overallPct%',
                    label: 'Average Score',
                    icon: Icons.star_rounded,
                    iconColor: const Color(0xFFF59E0B),
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

