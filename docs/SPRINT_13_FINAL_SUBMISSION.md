# SPRINT 13 — LearnSync AI Final Hackathon Submission & Production Hardening

## 1. Executive Summary

**LearnSync AI — Connecting Every Learner to Smarter Learning**

LearnSync AI is a phone-first, multimodal AI education platform designed to connect on-device & cloud AI tutoring on the student's smartphone with real-time classroom intelligence on the teacher's laptop dashboard.

---

## 2. Complete Architecture

```
                 Student Phone (iQOO Android)
                              │
                        LearnSync AI
                              │
                          AI Router
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   Local AI Engine       Gemini Cloud AI     Deterministic Offline
 Snapdragon NPU / QNN /       (Cloud)         Fallback Knowledge Base
 ONNX / TFLite / CPU
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
                       Learning Engine
                              │
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
   Student Phone                              Teacher Dashboard
        │                                           │
        └──────── Phone ↔ Laptop Office Kit ────────┘
```

---

## 3. Technology Stack

- **Student Mobile App**: Flutter (Dart), Material 3, Camera OCR, WebSockets, MethodChannel NPU Bridge.
- **Backend Infrastructure**: FastAPI (Python 3.12), Pydantic v2, WebSockets, Asyncio, Pytest.
- **Teacher Dashboard**: React 18, Vite, CSS, Lucide Icons, WebSockets + REST Polling Sync.
- **AI Routing Engine**: Unified `AIRouterService` (`AUTO` -> `LOCAL` -> `GEMINI` -> `FALLBACK`).
- **On-Device Hardware Bridge**: Native Android Kotlin MethodChannel (`DeviceCapabilityDetector`, `LocalInferenceBridge`).

---

## 4. Multimodal & Adaptive Capabilities Matrix

1. **Text AI Tutor**: Multi-turn dialogue with Simple, Real-World, and Technical explanation modes.
2. **Voice AI**: Speech recognition with state machine listening, transcribing, and speaking feedback.
3. **Camera Vision AI**: Snap homework questions, extract OCR text, confirm/edit, and generate step-by-step solutions.
4. **Adaptive Assessment Engine**: Real-time Item Response Theory (IRT) adjusting difficulty (Easy -> Medium -> Hard) dynamically.
5. **Learning Profile Engine**: Mastery score calculation (0–100%), weak topic detection, and targeted recommendations.
6. **Classroom Collaboration Layer**: Phone ↔ Laptop WebSocket event broadcasting & revision activity assignment.
7. **Local NPU & Offline AI**: On-device Snapdragon NPU capability detection with safe deterministic CPU fallback.

---

## 5. End-to-End Hackathon Demonstration Trajectory

1. **Student Ask**: Ask "Why does TCP use a three-way handshake?" -> Receive summary, simple explanation, real-world example, and follow-up chips.
2. **Voice Query**: Switch to Voice mode -> Ask "Explain TCP three-way handshake".
3. **Camera Question**: Scan problem "Solve 2x + 5 = 15" -> Extract OCR text -> Generate solution.
4. **Adaptive Assessment**: Take 5-question Operating Systems test -> Answer questions adaptively -> Detect weak topic "Process Scheduling" (58% mastery).
5. **Teacher Dashboard Live Feed**: Teacher dashboard receives real-time weak topic alert and misconception analysis.
6. **Targeted Revision Activity**: Teacher clicks "Create Revision Activity" for Process Scheduling -> Sends activity over WebSocket/REST.
7. **Student In-App Notification**: Student receives banner "Teacher Revision Activity Received" -> Taps "Start Revision" -> Launches targeted 5-question quiz.
8. **One-Tap Demo Reset**: Click "Reset Demo" on dashboard to restore initial pristine state.

---

## 6. Security & Credential Isolation

- Root `.gitignore` created excluding `.env`, `.env.*`, `__pycache__/`, `.dart_tool/`, `build/`, `dist/`, `node_modules/`, `.idea/`, `.vscode/`.
- Zero API keys or secrets in Flutter Dart source code.
- Zero API keys in React bundle.
- Credentials stored strictly in `backend/.env`.
- `/api/ai/status` exposes hardware capability flags without disclosing secrets.

---

## 7. Automated Test & Build Results

- **Backend Pytest Suite**: **61 passed in 1.57s** (100% pass rate across 11 test files).
- **React Teacher Dashboard**: Production build `npm run build` compiled clean in **1.13s**.
- **Secret Protection**: Verified zero API key or token leaks in response payloads.
