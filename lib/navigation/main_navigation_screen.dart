import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../features/assessment/assess_config_screen.dart';
import '../features/assessment/assess_screen.dart';
import '../features/assessment/assessment_question_screen.dart';
import '../features/assessment/assessment_result_screen.dart';
import '../features/camera/camera_question_screen.dart';
import '../features/camera/camera_result_screen.dart';
import '../features/home/home_screen.dart';
import '../features/learn/learn_screen.dart';
import '../features/profile/profile_screen.dart';
import '../features/progress/progress_screen.dart';
import '../features/tutor/ai_tutor_screen.dart';
import '../models/learning_models.dart';
import '../models/student_model.dart';
import '../services/assessment_service.dart';
import '../services/collaboration_service.dart';

enum OverlayRoute {
  none,
  aiTutor,
  cameraQuestion,
  cameraResult,
  voiceQuestion,
  assessConfig,
  assessmentQuestion,
  assessmentResult,
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentTabIndex = 0;
  OverlayRoute _overlay = OverlayRoute.none;

  final AssessmentService _assessmentService = AssessmentService();

  // Transient state for navigation parameters
  String? _tutorInitialQuery;
  List<Question>? _activeQuestions;
  String _activeSubject = 'Computer Networks';
  String _activeTopic = 'TCP';
  String _activeDifficulty = 'Adaptive';
  AssessmentResult? _activeResult;
  List<Map<String, dynamic>>? _activeSubmissions;
  List<String>? _activeAdaptivePath;

  void _navigateToTab(int index) {
    setState(() {
      _currentTabIndex = index;
      _overlay = OverlayRoute.none;
    });
  }

  void _openTutor([String? query]) {
    setState(() {
      _tutorInitialQuery = query;
      _overlay = OverlayRoute.aiTutor;
    });
  }

  void _openCamera() {
    setState(() {
      _overlay = OverlayRoute.cameraQuestion;
    });
  }

  void _openVoice() {
    setState(() {
      _overlay = OverlayRoute.voiceQuestion;
    });
  }

  void _startAssessmentConfig() {
    setState(() {
      _overlay = OverlayRoute.assessConfig;
    });
  }

  void _launchAssessment(String subject, String topic, String difficulty, int count) async {
    setState(() {
      _overlay = OverlayRoute.none;
    });

    final questions = await _assessmentService.generateAssessmentQuestions(
      subject: subject,
      topic: topic,
      difficulty: difficulty,
      questionCount: count,
    );

    if (!mounted) return;

    setState(() {
      _activeSubject = subject;
      _activeTopic = topic;
      _activeDifficulty = difficulty;
      _activeQuestions = questions;
      _overlay = OverlayRoute.assessmentQuestion;
    });
  }

  @override
  void initState() {
    super.initState();
    CollaborationService.instance.initialize();
  }

  void _submitAssessment(AssessmentResult result, List<Map<String, dynamic>> submissions, List<String> adaptivePath) async {
    // Update learning profile dynamically with recent assessment performance
    await LearningService().updateFromAssessment(
      subject: _activeSubject,
      topic: _activeTopic,
      percentage: result.percentage,
      submissions: submissions,
    );

    // Send real-time event to Teacher Dashboard via Collaboration Service
    CollaborationService.instance.sendStudentEvent(
      eventType: 'ASSESSMENT_COMPLETED',
      subject: _activeSubject,
      topic: _activeTopic,
      score: result.percentage,
      mastery: result.percentage,
      severity: result.percentage < 60 ? 'HIGH' : result.percentage < 80 ? 'MEDIUM' : 'LOW',
      payload: {'message': 'Completed assessment with score ${result.percentage}% on Student App'},
    );

    if (!mounted) return;

    setState(() {
      _activeResult = result;
      _activeSubmissions = submissions;
      _activeAdaptivePath = adaptivePath;
      _overlay = OverlayRoute.assessmentResult;
    });
  }

  void _handleRecommendationAction() {
    final nba = LearningService.currentProfile.nextBestAction;
    if (nba == null) {
      _openTutor('Revise TCP Connection Termination');
      return;
    }

    final String targetTopic = nba.subtopic ?? nba.topic;
    if (nba.action == 'practice' || nba.action == 'assessment') {
      _launchAssessment(nba.subject, targetTopic, nba.difficulty, 5);
    } else {
      _openTutor('Explain and revise $targetTopic step-by-step.');
    }
  }

  void _closeOverlay() {
    setState(() {
      _overlay = OverlayRoute.none;
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget body;

    // Handle full-screen prototype flows overlay
    switch (_overlay) {
      case OverlayRoute.aiTutor:
        body = AiTutorScreen(
          initialQuery: _tutorInitialQuery,
          onOpenCamera: _openCamera,
          onOpenVoice: _openVoice,
        );
        break;
      case OverlayRoute.cameraQuestion:
        body = CameraQuestionScreen(
          onBack: _closeOverlay,
          onAskTutor: (extractedQuestion, topic) {
            _openTutor(extractedQuestion);
          },
        );
        break;
      case OverlayRoute.cameraResult:
        body = CameraResultScreen(
          onBack: _closeOverlay,
          onGeneratePractice: () {
            _openTutor('Practice question for 2x + 5 = 15');
          },
        );
        break;
      case OverlayRoute.voiceQuestion:
        body = VoiceQuestionScreen(
          onCancel: _closeOverlay,
          onAskAi: (transcribed) {
            _openTutor(transcribed);
          },
        );
        break;
      case OverlayRoute.assessConfig:
        body = AssessConfigScreen(
          onBack: _closeOverlay,
          onStart: _launchAssessment,
        );
        break;
      case OverlayRoute.assessmentQuestion:
        if (_activeQuestions != null && _activeQuestions!.isNotEmpty) {
          body = AssessmentQuestionScreen(
            subject: _activeSubject,
            topic: _activeTopic,
            difficulty: _activeDifficulty,
            questions: _activeQuestions!,
            onCancel: _closeOverlay,
            onSubmitAssessment: _submitAssessment,
          );
        } else {
          body = const SizedBox.shrink();
        }
        break;
      case OverlayRoute.assessmentResult:
        if (_activeResult != null) {
          body = AssessmentResultScreen(
            result: _activeResult!,
            submissions: _activeSubmissions,
            adaptivePath: _activeAdaptivePath,
            onBackToAssessments: () {
              _navigateToTab(2); // Assess tab
            },
            onPracticeWeakTopic: (weakTopic) {
              _launchAssessment('Computer Networks', weakTopic, 'Easy', 5);
            },
            onUnderstandMistake: (mistake) {
              final qText = mistake['question_text'] ?? 'Question';
              final sel = mistake['selected_key'] ?? 'A';
              final cor = mistake['correct_key'] ?? 'B';
              final exp = mistake['explanation'] ?? '';
              _openTutor('Explain why I got this question wrong:\n\nQuestion: "$qText"\nMy Answer: $sel\nCorrect Answer: $cor\nExplanation: $exp');
            },
          );
        } else {
          body = const SizedBox.shrink();
        }
        break;
      case OverlayRoute.none:
      default:
        body = IndexedStack(
          index: _currentTabIndex,
          children: [
            HomeScreen(
              onNavigateToTab: _navigateToTab,
              onOpenTutor: _openTutor,
              onOpenCamera: _openCamera,
              onOpenVoice: _openVoice,
              onStartRevision: _handleRecommendationAction,
            ),
            LearnScreen(
              onSelectSubject: (subj) {
                _openTutor('Explain concepts in ${subj.title}');
              },
            ),
            AssessScreen(
              onOpenConfig: _startAssessmentConfig,
              onStartDirectAssessment: (assessment) {
                _launchAssessment(assessment.subjectName, 'TCP', assessment.difficulty, assessment.totalQuestions);
              },
            ),
            ProgressScreen(
              onStartRevision: _handleRecommendationAction,
            ),
            const ProfileScreen(),
          ],
        );
        break;
    }

    return Scaffold(
      body: ValueListenableBuilder<Map<String, dynamic>?>(
        valueListenable: CollaborationService.instance.pendingTeacherAction,
        builder: (context, action, child) {
          if (action == null) return body;
          final topic = action['topic'] ?? 'Process Scheduling';
          final subject = action['subject'] ?? 'Operating Systems';
          final msg = action['message'] ?? 'Your teacher sent you a revision activity.';
          final actionId = action['action_id'] ?? '';

          return Column(
            children: [
              MaterialBanner(
                backgroundColor: const Color(0xFFEEF2FF),
                elevation: 4,
                content: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.bolt_rounded, color: AppTheme.primary, size: 20),
                        SizedBox(width: 6),
                        Text(
                          'Teacher Revision Activity Received',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13.5, color: AppTheme.primaryDark),
                        ),
                      ],
                    ),
                    const SizedBox(height: 3),
                    Text(
                      '$msg ($subject — $topic)',
                      style: const TextStyle(fontSize: 12, color: Color(0xFF3730A3)),
                    ),
                  ],
                ),
                actions: [
                  TextButton(
                    onPressed: () {
                      CollaborationService.instance.acknowledgeAction(actionId);
                    },
                    child: const Text('Later', style: TextStyle(color: Colors.grey, fontSize: 12)),
                  ),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primary,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    onPressed: () {
                      CollaborationService.instance.acknowledgeAction(actionId);
                      _launchAssessment(subject, topic, 'Adaptive', 5);
                    },
                    child: const Text('Start Revision', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
              Expanded(child: body),
            ],
          );
        },
      ),
      bottomNavigationBar: _overlay != OverlayRoute.none
          ? null
          : BottomNavigationBar(
              currentIndex: _currentTabIndex,
              onTap: _navigateToTab,
              selectedItemColor: AppTheme.primary,
              unselectedItemColor: AppTheme.textSecondaryLight,
              items: const [
                BottomNavigationBarItem(
                  icon: Icon(Icons.home_outlined),
                  activeIcon: Icon(Icons.home_rounded),
                  label: 'Home',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.menu_book_outlined),
                  activeIcon: Icon(Icons.menu_book_rounded),
                  label: 'Learn',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.assignment_outlined),
                  activeIcon: Icon(Icons.assignment_rounded),
                  label: 'Assess',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.bar_chart_outlined),
                  activeIcon: Icon(Icons.bar_chart_rounded),
                  label: 'Progress',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.person_outline_rounded),
                  activeIcon: Icon(Icons.person_rounded),
                  label: 'Profile',
                ),
              ],
            ),
    );
  }
}
