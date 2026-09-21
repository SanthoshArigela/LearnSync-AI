# SPRINT 11 — LearnSync AI Final Production & Hackathon Readiness

## 1. Product Overview & Vision

**LearnSync AI — Connecting Every Learner to Smarter Learning**

LearnSync AI transforms the student's smartphone into a hyper-personalized, multimodal AI tutor while seamlessly connecting real-time classroom learning intelligence to the teacher's dashboard.

---

## 2. Solution Architecture

```
                 Student Phone (iQOO)
                          │
                    LearnSync AI
                          │
                      AI Router
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   On-Device AI        Gemini           Offline AI
  Snapdragon NPU        Cloud         Knowledge Base
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ↓
                   Learning Engine
                          │
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
   Student Phone                      Teacher Dashboard
        │                                   │
        └────── Phone ↔ Laptop Office Kit ──┘
```

---

## 3. Technology Stack

- **Student Mobile App**: Flutter (Dart), Material 3, Camera OCR, WebSockets, MethodChannel NPU Bridge.
- **Backend Infrastructure**: FastAPI (Python 3.12), Pydantic v2, WebSockets, Asyncio, Pytest.
- **Teacher Dashboard**: React 18, Vite, CSS, Lucide Icons, WebSockets + REST Polling Sync.
- **AI Engine Architecture**: Unified `AIRouterService` (`AUTO` -> `LOCAL` -> `GEMINI` -> `FALLBACK`).
- **On-Device Hardware Bridge**: Kotlin Native MethodChannel (`DeviceCapabilityDetector`, `LocalInferenceBridge`).

---

## 4. Multimodal & Adaptive Capabilities

1. **Text AI Tutor**: Multi-turn dialogue with Simple, Real-World, and Technical explanation modes.
2. **Voice AI**: Speech recognition with state machine listening, transcribing, and speaking indicator.
3. **Camera Vision AI**: Image question capture, OCR text extraction, question editing, and instant step-by-step solution.
4. **Adaptive Assessment Engine**: Real-time item response theory adjusting difficulty (Easy -> Medium -> Hard) dynamically.
5. **Learning Profile Engine**: Mastery score calculation (0–100%), weak topic detection, and targeted recommendations.
6. **Classroom Collaboration Layer**: Phone ↔ Laptop WebSocket event broadcasting & revision activity assignment.
7. **Local NPU & Offline AI**: On-device Snapdragon NPU capability detection with safe deterministic CPU fallback.

---

## 5. End-to-End Demonstration Walkthrough

1. **Student Ask**: Ask "Why does TCP use a three-way handshake?" -> Receive summary, simple explanation, real-world example, and follow-up chips.
2. **Voice Query**: Switch to Voice mode -> Ask "Explain TCP three-way handshake".
3. **Camera Question**: Scan problem "Solve 2x + 5 = 15" -> Extract OCR text -> Generate solution.
4. **Adaptive Assessment**: Take 5-question Operating Systems test -> Answer questions adaptively -> Detect weak topic "Process Scheduling" (58% mastery).
5. **Teacher Dashboard Live Feed**: Teacher dashboard receives real-time weak topic alert and misconception analysis.
6. **Targeted Revision Activity**: Teacher clicks "Create Revision Activity" for Process Scheduling -> Sends activity over WebSocket/REST.
7. **Student In-App Notification**: Student receives banner "Your teacher sent you a revision activity" -> Taps "Start Revision" -> Launches targeted 5-question quiz.
8. **One-Tap Demo Reset**: Click "Reset Demo" on dashboard to restore initial pristine state.

---

## 6. Security & Credential Isolation

- Zero API keys or secrets in Flutter Dart source.
- Zero API keys in React bundle.
- Credentials stored strictly in `backend/.env`.
- `/api/ai/status` exposes hardware capability flags without disclosing secrets.

---

## 7. Verification Summary

- **Backend Pytest Suite**: `55 passed in 1.43s` (100% pass rate).
- **React Teacher Dashboard**: Production build `npm run build` compiled clean in `904ms`.
- **Flutter Static Analysis**: `flutter analyze` clean.
- **Physical LAN & iQOO Readiness**: IP address configurable via `ApiConfig.baseUrl`.
