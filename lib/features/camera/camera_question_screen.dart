import 'dart:typed_data';
import 'package:flutter/material.dart';
import '../../core/constants/app_strings.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/reusable_widgets.dart';
import '../../services/vision_service.dart';

class CameraQuestionScreen extends StatefulWidget {
  final VoidCallback onBack;
  final Function(String extractedQuestion, String topic) onAskTutor;

  const CameraQuestionScreen({
    super.key,
    required this.onBack,
    required this.onAskTutor,
  });

  @override
  State<CameraQuestionScreen> createState() => _CameraQuestionScreenState();
}

class _CameraQuestionScreenState extends State<CameraQuestionScreen> {
  final VisionService _visionService = VisionService();
  final TextEditingController _questionTextController = TextEditingController();

  bool _isCaptured = false;
  bool _isAnalyzing = false;
  bool _isFlashOn = false;
  bool _permissionDenied = false;
  String? _errorMessage;

  ExtractedQuestionResult? _extractedResult;

  @override
  void dispose() {
    _questionTextController.dispose();
    super.dispose();
  }

  void _triggerCapture() async {
    setState(() {
      _isCaptured = true;
      _isAnalyzing = true;
      _errorMessage = null;
    });

    // Simulate capturing 1x1 dummy pixel bytes for memory-based vision analysis
    final dummyBytes = Uint8List.fromList([137, 80, 78, 71, 13, 10, 26, 10]);

    try {
      final res = await _visionService.analyzeImageBytes(dummyBytes);

      if (!mounted) return;

      setState(() {
        _isAnalyzing = false;
        _extractedResult = res;
        _questionTextController.text = res.question;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isAnalyzing = false;
        _errorMessage = 'The image is difficult to read. Try capturing with better lighting.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_permissionDenied) {
      return _buildPermissionDeniedView();
    }

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_rounded, color: Colors.white),
          onPressed: widget.onBack,
        ),
        title: const Text(
          AppStrings.cameraTitle,
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            icon: Icon(
              _isFlashOn ? Icons.flash_on_rounded : Icons.flash_off_rounded,
              color: _isFlashOn ? Colors.amber : Colors.white,
            ),
            onPressed: () {
              setState(() {
                _isFlashOn = !_isFlashOn;
              });
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Top Instruction Banner
            Container(
              width: double.infinity,
              color: Colors.black87,
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Text(
                _isCaptured
                    ? 'Review and edit the detected question below.'
                    : AppStrings.cameraInstruction,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white70, fontSize: 13),
              ),
            ),

            // Camera Viewfinder & OCR Result Container
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(24),
                      border: Border.all(
                        color: _isCaptured ? AppTheme.primary : Colors.white30,
                        width: 2,
                      ),
                    ),
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        if (!_isCaptured) ...[
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: const [
                              Icon(Icons.camera_alt_outlined, size: 64, color: Colors.white38),
                              SizedBox(height: 12),
                              Text(
                                'Align question within frame',
                                style: TextStyle(color: Colors.white38, fontSize: 14),
                              ),
                            ],
                          ),
                          Positioned(
                            top: 40,
                            left: 40,
                            right: 40,
                            bottom: 40,
                            child: Container(
                              decoration: BoxDecoration(
                                border: Border.all(color: Colors.white.withOpacity(0.4), width: 1.5),
                                borderRadius: BorderRadius.circular(16),
                              ),
                            ),
                          ),
                        ] else if (_isAnalyzing) ...[
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: const [
                              CircularProgressIndicator(color: AppTheme.primary),
                              SizedBox(height: 16),
                              Text(
                                'LearnSync AI is analyzing your question...',
                                style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                              ),
                              SizedBox(height: 4),
                              Text(
                                'Reading image → Understanding topic',
                                style: TextStyle(color: Colors.white54, fontSize: 12),
                              ),
                            ],
                          ),
                        ] else ...[
                          // OCR Question Confirmation Panel
                          SingleChildScrollView(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: const [
                                    Icon(Icons.check_circle_rounded, color: AppTheme.success, size: 20),
                                    SizedBox(width: 8),
                                    Text(
                                      'Question Detected',
                                      style: TextStyle(
                                        color: AppTheme.success,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 14,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 12),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: AppTheme.primary.withOpacity(0.2),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    'Topic: ${_extractedResult?.topic ?? "Mathematics"} (${_extractedResult?.contentType.toUpperCase() ?? "EQUATION"})',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 16),

                                // Editable Text Field
                                Container(
                                  width: double.infinity,
                                  padding: const EdgeInsets.all(14),
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(16),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            'Extracted Question (Tap to edit):',
                                            style: TextStyle(
                                              color: AppTheme.textSecondaryLight,
                                              fontSize: 11,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                          Icon(Icons.edit_outlined, size: 14, color: AppTheme.primary),
                                        ],
                                      ),
                                      const SizedBox(height: 6),
                                      TextField(
                                        controller: _questionTextController,
                                        maxLines: 3,
                                        style: const TextStyle(
                                          color: AppTheme.textPrimaryLight,
                                          fontSize: 16,
                                          fontWeight: FontWeight.bold,
                                        ),
                                        decoration: const InputDecoration(
                                          border: InputBorder.none,
                                          contentPadding: EdgeInsets.zero,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
            ),

            // Bottom Actions
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
              color: Colors.black,
              child: _isCaptured && !_isAnalyzing
                  ? Row(
                      children: [
                        Expanded(
                          child: SecondaryButton(
                            label: 'Retake',
                            onPressed: () {
                              setState(() {
                                _isCaptured = false;
                                _extractedResult = null;
                              });
                            },
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: PrimaryButton(
                            label: 'Ask LearnSync AI',
                            icon: Icons.auto_awesome,
                            onPressed: () {
                              widget.onAskTutor(
                                _questionTextController.text,
                                _extractedResult?.topic ?? 'Mathematics',
                              );
                            },
                          ),
                        ),
                      ],
                    )
                  : Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.photo_library_outlined,
                              color: Colors.white, size: 28),
                          onPressed: _triggerCapture,
                        ),
                        GestureDetector(
                          onTap: _triggerCapture,
                          child: Container(
                            width: 72,
                            height: 72,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              border: Border.all(color: Colors.white, width: 4),
                            ),
                            child: Center(
                              child: Container(
                                width: 56,
                                height: 56,
                                decoration: const BoxDecoration(
                                  color: Colors.white,
                                  shape: BoxShape.circle,
                                ),
                              ),
                            ),
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.flip_camera_ios_outlined,
                              color: Colors.white, size: 28),
                          onPressed: () {},
                        ),
                      ],
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPermissionDeniedView() {
    return Scaffold(
      backgroundColor: AppTheme.backgroundLight,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_rounded),
          onPressed: widget.onBack,
        ),
        title: const Text('Camera Access Required'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.camera_enhance_outlined, size: 64, color: AppTheme.primary),
              const SizedBox(height: 16),
              const Text(
                'Camera permission required',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              const Text(
                'LearnSync AI needs camera access to understand questions from your study material.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 13, color: AppTheme.textSecondaryLight),
              ),
              const SizedBox(height: 24),
              PrimaryButton(
                label: 'Allow Camera Access',
                icon: Icons.check_rounded,
                onPressed: () {
                  setState(() {
                    _permissionDenied = false;
                  });
                },
              ),
              const SizedBox(height: 12),
              SecondaryButton(
                label: 'Ask by Text Instead',
                onPressed: widget.onBack,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
