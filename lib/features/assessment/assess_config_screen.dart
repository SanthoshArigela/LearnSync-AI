import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';

class AssessConfigScreen extends StatefulWidget {
  final VoidCallback onBack;
  final Function(String subject, String topic, String difficulty, int count) onStart;

  const AssessConfigScreen({
    super.key,
    required this.onBack,
    required this.onStart,
  });

  @override
  State<AssessConfigScreen> createState() => _AssessConfigScreenState();
}

class _AssessConfigScreenState extends State<AssessConfigScreen> {
  String _selectedSubject = 'Computer Networks';
  String _selectedTopic = 'TCP';
  String _selectedDifficulty = 'Adaptive'; // 'Easy', 'Medium', 'Hard', 'Adaptive'
  int _questionCount = 5;

  final Map<String, List<String>> _topicsBySubject = {
    'Computer Networks': ['TCP', 'UDP', 'DNS', 'OSI Model', 'HTTP'],
    'Data Structures': ['Arrays', 'Linked Lists', 'Stacks', 'Queues', 'Trees'],
    'DBMS': ['Normalization', 'Keys', 'SQL', 'ACID Transactions'],
    'Operating Systems': ['Process Scheduling', 'Processes', 'Threads', 'Deadlocks'],
    'Machine Learning': ['Linear Regression', 'Neural Networks', 'Clustering'],
  };

  @override
  Widget build(BuildContext context) {
    final availableTopics = _topicsBySubject[_selectedSubject] ?? ['General'];

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_rounded),
          onPressed: widget.onBack,
        ),
        title: const Text('Start AI Assessment'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFEEF2FF),
                  borderRadius: BorderRadius.circular(18),
                  border: Border.all(color: const Color(0xFFC7D2FE)),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: const BoxDecoration(
                        color: AppTheme.primary,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.auto_awesome, color: Colors.white, size: 20),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text(
                            'AI Adaptive Assessment',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 15,
                              color: AppTheme.primaryDark,
                            ),
                          ),
                          SizedBox(height: 2),
                          Text(
                            'LearnSync AI will adjust question difficulty based on your live answers.',
                            style: TextStyle(fontSize: 12.5, color: Color(0xFF4338CA)),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),

              // Subject Selector
              const Text(
                'Select Subject',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: AppTheme.cardBorder),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: _selectedSubject,
                    isExpanded: true,
                    items: _topicsBySubject.keys.map((subj) {
                      return DropdownMenuItem(value: subj, child: Text(subj));
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) {
                        setState(() {
                          _selectedSubject = val;
                          _selectedTopic = _topicsBySubject[val]!.first;
                        });
                      }
                    },
                  ),
                ),
              ),
              const SizedBox(height: 18),

              // Topic Selector
              const Text(
                'Select Topic',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: availableTopics.map((top) {
                  final isSel = _selectedTopic == top;
                  return ChoiceChip(
                    label: Text(top),
                    selected: isSel,
                    selectedColor: AppTheme.primary,
                    backgroundColor: AppTheme.backgroundLight,
                    labelStyle: TextStyle(
                      color: isSel ? Colors.white : AppTheme.textPrimaryLight,
                      fontWeight: FontWeight.bold,
                    ),
                    onSelected: (selected) {
                      if (selected) {
                        setState(() {
                          _selectedTopic = top;
                        });
                      }
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 18),

              // Difficulty Selector
              const Text(
                'Select Difficulty Mode',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Row(
                children: ['Easy', 'Medium', 'Hard', 'Adaptive'].map((diff) {
                  final isSel = _selectedDifficulty == diff;
                  return Expanded(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 3),
                      child: ChoiceChip(
                        label: Text(diff, style: const TextStyle(fontSize: 12)),
                        selected: isSel,
                        selectedColor: AppTheme.primary,
                        backgroundColor: AppTheme.backgroundLight,
                        labelStyle: TextStyle(
                          color: isSel ? Colors.white : AppTheme.textPrimaryLight,
                          fontWeight: FontWeight.bold,
                        ),
                        onSelected: (selected) {
                          if (selected) {
                            setState(() {
                              _selectedDifficulty = diff;
                            });
                          }
                        },
                      ),
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 18),

              // Question Count Selector
              const Text(
                'Number of Questions',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Row(
                children: [5, 10].map((cnt) {
                  final isSel = _questionCount == cnt;
                  return Padding(
                    padding: const EdgeInsets.only(right: 12),
                    child: ChoiceChip(
                      label: Text('$cnt Questions'),
                      selected: isSel,
                      selectedColor: AppTheme.primary,
                      backgroundColor: AppTheme.backgroundLight,
                      labelStyle: TextStyle(
                        color: isSel ? Colors.white : AppTheme.textPrimaryLight,
                        fontWeight: FontWeight.bold,
                      ),
                      onSelected: (selected) {
                        if (selected) {
                          setState(() {
                            _questionCount = cnt;
                          });
                        }
                      },
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 32),

              // Start Button
              PrimaryButton(
                label: 'Start Assessment',
                icon: Icons.play_arrow_rounded,
                onPressed: () {
                  widget.onStart(
                    _selectedSubject,
                    _selectedTopic,
                    _selectedDifficulty,
                    _questionCount,
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
