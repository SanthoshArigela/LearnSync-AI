import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../data/mock/mock_data_service.dart';
import '../../models/student_model.dart';

class LearnScreen extends StatefulWidget {
  final Function(Subject subject) onSelectSubject;

  const LearnScreen({
    super.key,
    required this.onSelectSubject,
  });

  @override
  State<LearnScreen> createState() => _LearnScreenState();
}

class _LearnScreenState extends State<LearnScreen> {
  String _searchQuery = '';
  List<Subject> _filteredSubjects = MockDataService.subjects;

  void _onSearchChanged(String query) {
    setState(() {
      _searchQuery = query;
      _filteredSubjects = MockDataService.subjects
          .where((s) => s.title.toLowerCase().contains(query.toLowerCase()))
          .toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Learning'),
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Search Input
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.cardBorder),
                ),
                child: TextField(
                  onChanged: _onSearchChanged,
                  decoration: const InputDecoration(
                    hintText: 'Search subjects or topics',
                    prefixIcon: Icon(Icons.search_rounded, color: AppTheme.textSecondaryLight),
                    border: InputBorder.none,
                    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              Text(
                'Enrolled Subjects (${_filteredSubjects.length})',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textPrimaryLight,
                ),
              ),
              const SizedBox(height: 12),

              // Subject List
              Expanded(
                child: _filteredSubjects.isEmpty
                    ? const EmptyStateWidget(
                        title: 'No Subjects Found',
                        message: 'Try searching for another topic or subject.',
                      )
                    : ListView.builder(
                        itemCount: _filteredSubjects.length,
                        itemBuilder: (context, index) {
                          final subject = _filteredSubjects[index];
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 12),
                            child: SubjectCard(
                              title: subject.title,
                              totalTopics: subject.totalTopics,
                              progressPercentage: subject.progressPercentage,
                              onContinue: () => widget.onSelectSubject(subject),
                            ),
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
}
