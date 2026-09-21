import 'package:flutter/material.dart';
import '../../core/constants/app_strings.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../services/speech_service.dart';

class VoiceQuestionScreen extends StatefulWidget {
  final VoidCallback onCancel;
  final Function(String transcribedText) onAskAi;

  const VoiceQuestionScreen({
    super.key,
    required this.onCancel,
    required this.onAskAi,
  });

  @override
  State<VoiceQuestionScreen> createState() => _VoiceQuestionScreenState();
}

class _VoiceQuestionScreenState extends State<VoiceQuestionScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  final TextEditingController _editController = TextEditingController();
  bool _isEditing = false;

  final SpeechService _speechService = SpeechService.instance;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    )..repeat(reverse: true);

    _speechService.startListening();

    _speechService.transcribedText.addListener(() {
      if (_speechService.transcribedText.value.isNotEmpty) {
        _editController.text = _speechService.transcribedText.value;
      }
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _editController.dispose();
    super.dispose();
  }

  void _handleMicTap() {
    final curState = _speechService.state.value;
    if (curState == VoiceState.listening) {
      _speechService.stopListening();
    } else {
      setState(() {
        _isEditing = false;
      });
      _speechService.startListening();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.close_rounded),
          onPressed: widget.onCancel,
        ),
        title: const Text('Ask LearnSync AI by Voice'),
      ),
      body: SafeArea(
        child: ValueListenableBuilder<VoiceState>(
          valueListenable: _speechService.state,
          builder: (context, voiceState, child) {
            final isListening = voiceState == VoiceState.listening;
            final isProcessing = voiceState == VoiceState.processing || voiceState == VoiceState.transcribing;

            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Instruction Header
                  Column(
                    children: [
                      const SizedBox(height: 12),
                      Text(
                        isListening
                            ? 'Listening... Speak your question naturally.'
                            : isProcessing
                                ? 'Transcribing your question into text...'
                                : 'Question captured! Verify or edit before asking AI.',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          color: AppTheme.textSecondaryLight,
                          height: 1.4,
                        ),
                      ),
                    ],
                  ),

                  // Central Pulsing Microphone / Status
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      AnimatedBuilder(
                        animation: _pulseController,
                        builder: (context, child) {
                          final scale = isListening ? 1.0 + (_pulseController.value * 0.15) : 1.0;
                          return Transform.scale(
                            scale: scale,
                            child: Container(
                              width: 140,
                              height: 140,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: isListening
                                    ? AppTheme.primary.withOpacity(0.15)
                                    : isProcessing
                                        ? Colors.orange.withOpacity(0.15)
                                        : AppTheme.success.withOpacity(0.15),
                                border: Border.all(
                                  color: isListening
                                      ? AppTheme.primary.withOpacity(0.4)
                                      : isProcessing
                                          ? Colors.orange.withOpacity(0.4)
                                          : AppTheme.success.withOpacity(0.4),
                                  width: 2,
                                ),
                              ),
                              child: Center(
                                child: Material(
                                  color: isListening
                                      ? AppTheme.primary
                                      : isProcessing
                                          ? Colors.orange
                                          : AppTheme.success,
                                  shape: const CircleBorder(),
                                  elevation: 8,
                                  child: InkWell(
                                    customBorder: const CircleBorder(),
                                    onTap: _handleMicTap,
                                    child: Padding(
                                      padding: const EdgeInsets.all(28),
                                      child: Icon(
                                        isListening ? Icons.mic_rounded : Icons.mic_none_rounded,
                                        size: 48,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 20),

                      // Status Badge
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: isListening
                              ? AppTheme.primary.withOpacity(0.1)
                              : isProcessing
                                  ? Colors.orange.withOpacity(0.1)
                                  : AppTheme.success.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              width: 8,
                              height: 8,
                              decoration: BoxDecoration(
                                color: isListening
                                    ? AppTheme.primary
                                    : isProcessing
                                        ? Colors.orange
                                        : AppTheme.success,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              isListening
                                  ? 'Listening...'
                                  : isProcessing
                                      ? 'Processing Audio...'
                                      : 'Ready to Ask',
                              style: TextStyle(
                                color: isListening
                                    ? AppTheme.primary
                                    : isProcessing
                                        ? Colors.orange[900]
                                        : AppTheme.success,
                                fontWeight: FontWeight.bold,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),

                  // Transcribed Text Box & Actions
                  Column(
                    children: [
                      ValueListenableBuilder<String>(
                        valueListenable: _speechService.transcribedText,
                        builder: (context, textVal, child) {
                          final displayText = textVal.isNotEmpty
                              ? textVal
                              : 'Why does TCP use a three-way handshake?';

                          return Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(16),
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
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Row(
                                      children: const [
                                        Icon(Icons.record_voice_over_outlined,
                                            size: 18, color: AppTheme.textSecondaryLight),
                                        SizedBox(width: 8),
                                        Text(
                                          'Transcribed Question:',
                                          style: TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.bold,
                                            color: AppTheme.textSecondaryLight,
                                          ),
                                        ),
                                      ],
                                    ),
                                    InkWell(
                                      onTap: () {
                                        setState(() {
                                          _isEditing = !_isEditing;
                                        });
                                      },
                                      child: Text(
                                        _isEditing ? 'Done' : 'Edit Text',
                                        style: const TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.bold,
                                          color: AppTheme.primary,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                _isEditing
                                    ? TextField(
                                        controller: _editController,
                                        style: const TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.w600,
                                          color: AppTheme.textPrimaryLight,
                                        ),
                                        decoration: const InputDecoration(
                                          border: InputBorder.none,
                                          isDense: true,
                                        ),
                                      )
                                    : Text(
                                        displayText,
                                        style: const TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.w600,
                                          color: AppTheme.textPrimaryLight,
                                          height: 1.3,
                                        ),
                                      ),
                              ],
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 18),

                      Row(
                        children: [
                          Expanded(
                            child: SecondaryButton(
                              label: AppStrings.cancel,
                              onPressed: widget.onCancel,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: PrimaryButton(
                              label: 'Ask LearnSync AI',
                              icon: Icons.auto_awesome,
                              onPressed: () {
                                final text = _editController.text.isNotEmpty
                                    ? _editController.text
                                    : 'Why does TCP use a three-way handshake?';
                                widget.onAskAi(text);
                              },
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                    ],
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
