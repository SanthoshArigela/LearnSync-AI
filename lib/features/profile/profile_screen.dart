import 'package:flutter/material.dart';
import '../../core/constants/app_strings.dart';
import '../../core/theme/app_theme.dart';
import '../../services/auth_service.dart';
import '../auth/login_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Profile'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
          child: Column(
            children: [
              // User Avatar & Info Header
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppTheme.cardBorder),
                ),
                child: Column(
                  children: [
                    CircleAvatar(
                      radius: 40,
                      backgroundColor: AppTheme.primary,
                      child: const Text(
                        'S',
                        style: TextStyle(
                          fontSize: 36,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      AppStrings.studentName,
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textPrimaryLight,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppTheme.primary.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Text(
                        AppStrings.studentDegree,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.primary,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Profile Section Items
              _buildSectionCard(
                title: 'My Subjects',
                icon: Icons.book_rounded,
                subtitle: '5 enrolled subjects (CSE Core)',
                onTap: () {
                  _showSnack(context, 'Managing enrolled subjects');
                },
              ),
              const SizedBox(height: 10),
              _buildSectionCard(
                title: 'Learning Preferences',
                icon: Icons.tune_rounded,
                subtitle: 'Pacing: Standard | AI Explanation: Balanced',
                onTap: () {
                  _showSnack(context, 'Opening Learning Preferences');
                },
              ),
              const SizedBox(height: 10),
              _buildSectionCard(
                title: 'Notifications',
                icon: Icons.notifications_none_rounded,
                subtitle: 'Daily revision reminders & quiz alerts enabled',
                onTap: () {
                  _showSnack(context, 'Opening Notification Settings');
                },
              ),
              const SizedBox(height: 10),
              _buildSectionCard(
                title: 'About LearnSync AI',
                icon: Icons.info_outline_rounded,
                subtitle: AppStrings.tagline,
                onTap: () {
                  showAboutDialog(
                    context: context,
                    applicationName: AppStrings.appName,
                    applicationVersion: 'v1.0.0 (Sprint 1 Prototype)',
                    applicationIcon: const Icon(Icons.auto_awesome, color: AppTheme.primary, size: 36),
                    children: const [
                      Text(AppStrings.tagline),
                      SizedBox(height: 10),
                      Text('LearnSync AI Intelligent Learning Platform — Connecting Every Learner to Smarter Learning.'),
                    ],
                  );
              const SizedBox(height: 12),
              _buildSectionCard(
                title: 'Sign Out',
                icon: Icons.logout_rounded,
                subtitle: 'Clear session & return to login',
                onTap: () {
                  AuthService.logout();
                  Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute(builder: (_) => const LoginScreen()),
                    (route) => false,
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionCard({
    required String title,
    required IconData icon,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.cardBorder),
      ),
      child: ListTile(
        onTap: onTap,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppTheme.primary.withOpacity(0.1),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(icon, color: AppTheme.primary),
        ),
        title: Text(
          title,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
        ),
        subtitle: Text(
          subtitle,
          style: const TextStyle(fontSize: 12, color: AppTheme.textSecondaryLight),
        ),
        trailing: const Icon(Icons.chevron_right_rounded, color: AppTheme.textSecondaryLight),
      ),
    );
  }

  void _showSnack(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), duration: const Duration(seconds: 2)),
    );
  }
}
