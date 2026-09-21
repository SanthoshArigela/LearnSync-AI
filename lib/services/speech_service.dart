import 'dart:async';
import 'package:flutter/foundation.dart';

enum VoiceState {
  idle,
  listening,
  processing,
  transcribing,
  completed,
  error,
}

class SpeechService {
  static final SpeechService instance = SpeechService._internal();

  factory SpeechService() => instance;

  SpeechService._internal();

  final ValueNotifier<VoiceState> state = ValueNotifier<VoiceState>(VoiceState.idle);
  final ValueNotifier<String> transcribedText = ValueNotifier<String>('');
  final ValueNotifier<double> soundLevel = ValueNotifier<double>(0.0);

  Timer? _simulationTimer;

  void startListening({String? mockPresetText}) {
    state.value = VoiceState.listening;
    transcribedText.value = '';
    soundLevel.value = 0.5;

    _simulationTimer?.cancel();
    _simulationTimer = Timer(const Duration(seconds: 2), () {
      state.value = VoiceState.processing;
      soundLevel.value = 0.2;

      _simulationTimer = Timer(const Duration(seconds: 1), () {
        state.value = VoiceState.transcribing;
        transcribedText.value = mockPresetText ?? 'Why does TCP use a three-way handshake?';

        _simulationTimer = Timer(const Duration(milliseconds: 500), () {
          state.value = VoiceState.completed;
          soundLevel.value = 0.0;
        });
      });
    });
  }

  void stopListening() {
    _simulationTimer?.cancel();
    if (transcribedText.value.isEmpty) {
      transcribedText.value = 'Why does TCP use a three-way handshake?';
    }
    state.value = VoiceState.completed;
  }

  void reset() {
    _simulationTimer?.cancel();
    state.value = VoiceState.idle;
    transcribedText.value = '';
    soundLevel.value = 0.0;
  }

  void dispose() {
    _simulationTimer?.cancel();
  }
}
