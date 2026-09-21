import 'package:flutter/material.dart';
import '../../core/constants/app_strings.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../data/mock/mock_data_service.dart';
import '../../models/learning_models.dart';
import '../../services/learning_service.dart';
import '../../services/collaboration_service.dart';

class HomeScreen extends StatelessWidget {
  final Function(int index) onNavigateToTab;
  final VoidCallback onOpenTutor;
  final VoidCallback onOpenCamera;
  final VoidCallback onOpenVoice;
  final VoidCallback onStartRevision;

  const HomeScreen({
    super.key,
    required this.onNavigateToTab,
    required this.onOpenTutor,
    required this.onOpenCamera,
    required this.onOpenVoice,
    required this.onStartRevision,
  });

  @override
  Widget build(BuildContext context) {
    final profile = LearningService.currentProfile;
    final nba = profile.nextBestAction;

    final recTitle = nba?.title ?? AppStrings.recTitle;
    final recDesc = nba?.reason ?? AppStrings.recDesc;
    final recButtonLabel = nba?.action == 'practice'
        ? 'Practice Weak Topic'
        : (nba?.action == 'assessment' ? 'Take Assessment' : AppStrings.recButton);

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Text(
                            AppStrings.studentGreeting,
                            style: TextStyle(
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.textPrimaryLight,
                            ),
                          ),
                          const SizedBox(width: 8),
                          ValueListenableBuilder<bool>(
                            valueListenable: CollaborationService.instance.isConnected,
                            builder: (context, connected, child) {
                              return Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                decoration: BoxDecoration(
                                  color: connected ? const Color(0xFFD1FAE5) : const Color(0xFFFEF3C7),
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(color: connected ? const Color(0xFF6EE7B7) : const Color(0xFFFCD34D)),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Container(
                                      width: 6,
                                      height: 6,
                                      decoration: BoxDecoration(
                                        color: connected ? const Color(0xFF059669) : const Color(0xFFD97706),
                                        shape: BoxShape.circle,
                                      ),
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      connected ? 'Sync Connected' : 'Syncing...',
                                      style: TextStyle(
                                        fontSize: 10,
                                        fontWeight: FontWeight.bold,
                                        color: connected ? const Color(0xFF065F46) : const Color(0xFF92400E),
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            },
                          ),
                        ],
                      ),
                      const SizedBox(height: 2),
                      const Text(
                        AppStrings.studentSubtitle,
                        style: TextStyle(
                          fontSize: 14,
                          color: AppTheme.textSecondaryLight,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                      border: Border.all(color: AppTheme.cardBorder),
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.notifications_none_rounded),
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                                'Notifications: ${profile.recommendations.length} active learning recommendations'),
                            duration: const Duration(seconds: 2),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              // AI Tutor Banner Card
              AiCard(
                title: AppStrings.aiTutorTitle,
                subtitle: AppStrings.aiTutorSubtitle,
                onAskQuestion: onOpenTutor,
                onScanQuestion: onOpenCamera,
                onAskByVoice: onOpenVoice,
              ),
              const SizedBox(height: 22),

              // Continue Learning
              _buildContinueLearningCard(context),
              const SizedBox(height: 22),

              // Today's Progress
              const Text(
                AppStrings.todaysProgressTitle,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: StatisticCard(
                      value: AppStrings.learningTimeVal,
                      label: AppStrings.learningTimeLabel,
                      icon: Icons.timer_outlined,
                      iconColor: AppTheme.primary,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: StatisticCard(
                      value: AppStrings.questionsAskedVal,
                      label: AppStrings.questionsAskedLabel,
                      icon: Icons.help_outline_rounded,
                      iconColor: AppTheme.secondary,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              StatisticCard(
                value: '${profile.overallMastery}%',
                label: AppStrings.avgScoreLabel,
                icon: Icons.emoji_events_outlined,
                iconColor: const Color(0xFFF59E0B),
              ),
              const SizedBox(height: 22),

              // AI Recommendation (Next Best Action)
              RecommendationCard(
                badgeText: AppStrings.recommendedForYou,
                title: recTitle,
                description: recDesc,
                buttonText: recButtonLabel,
                onAction: onStartRevision,
              ),
              const SizedBox(height: 22),

              // Your Learning Insights Card (Sprint 5 Requirement 28)
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppTheme.cardBorder),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.03),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.lightbulb_rounded, color: AppTheme.primary, size: 22),
                        SizedBox(width: 8),
                        Text(
                          'Your Learning Insights',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: AppTheme.textPrimaryLight,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        const Icon(Icons.check_circle_outline_rounded, color: Colors.green, size: 16),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            'Strong in: ${profile.strongTopics.isNotEmpty ? profile.strongTopics.first : "TCP Basics"}',
                            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        const Icon(Icons.trending_up_rounded, color: AppTheme.primary, size: 16),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            'Improving in: ${profile.moderateTopics.isNotEmpty ? profile.moderateTopics.first : "TCP Handshake"}',
                            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        const Icon(Icons.warning_amber_rounded, color: Colors.orange, size: 16),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            'Needs practice in: ${profile.weakTopics.isNotEmpty ? profile.weakTopics.first : "TCP Connection Termination"}',
                            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.orange),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),

              // Subject Overview
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Subject Overview',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  TextButton(
                    onPressed: () => onNavigateToTab(1), // Go to Learn tab
                    child: const Text(
                      'View All',
                      style: TextStyle(
                        color: AppTheme.primary,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              ...(profile.subjects.isNotEmpty
                      ? profile.subjects.values.take(3)
                      : MockDataService.subjects.take(3))
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
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: AppTheme.primary.withOpacity(0.1),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(
                              Icons.folder_open_rounded,
                              color: AppTheme.primary,
                              size: 20,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  title,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(4),
                                  child: LinearProgressIndicator(
                                    value: mastery / 100.0,
                                    minHeight: 6,
                                    backgroundColor: AppTheme.cardBorder,
                                    valueColor: AlwaysStoppedAnimation<Color>(
                                      mastery < 60 ? Colors.orange : AppTheme.primary,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 14),
                          Text(
                            '$mastery%',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: mastery < 60 ? Colors.orange : AppTheme.primary,
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildContinueLearningCard(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppTheme.cardBorder),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                AppStrings.continueLearningTitle,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.textSecondaryLight,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppTheme.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Text(
                  '${AppStrings.defaultProgress}% Done',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.primary,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          const Text(
            AppStrings.defaultSubject,
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 2),
          const Text(
            'Current Topic: ${AppStrings.defaultTopic}',
            style: TextStyle(
              fontSize: 14,
              color: AppTheme.textSecondaryLight,
            ),
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: const LinearProgressIndicator(
              value: AppStrings.defaultProgress / 100.0,
              minHeight: 8,
              backgroundColor: AppTheme.cardBorder,
              valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primary),
            ),
          ),
          const SizedBox(height: 16),
          PrimaryButton(
            label: 'Continue Learning',
            icon: Icons.play_arrow_rounded,
            onPressed: () => onNavigateToTab(1), // Open Learn Tab
          ),
        ],
      ),
    );
  }
}
