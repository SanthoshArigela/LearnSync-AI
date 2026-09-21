# SPRINT 14 — Physical iQOO Device Validation & Rehearsal Report

## 1. Physical Device Environment & Android Permissions

- **Target Smartphone**: iQOO Android Smartphone Platform
- **Network Protocol**: Wi-Fi / Local Area Network (LAN)
- **Host Binding**: `0.0.0.0:8000` (FastAPI)
- **Base URL Config**: Configurable dynamically via `ApiConfig.baseUrl` in Flutter app.
- **Cleartext Traffic**: Enabled via `android:usesCleartextTraffic="true"` in `android/app/src/main/AndroidManifest.xml`.

### Android Permissions Verified (`AndroidManifest.xml`)
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`
- `android.permission.CAMERA`
- `android.permission.RECORD_AUDIO`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.READ_MEDIA_IMAGES`

---

## 2. On-Device NPU & MethodChannel Capability Bridge

Native Kotlin MethodChannel `com.learnsync.ai/npu_bridge` communicates safely between Flutter and Android:

- **`DeviceCapabilityDetector.kt`**: Evaluates SoC manufacturer (`qcom`/`snapdragon`), Hexagon NPU libraries, and model path (`/sdcard/Android/data/.../models/learnsync_slm.bin`).
- **`LocalInferenceBridge.kt`**: Handles capability queries safely without crashing on unsupported platforms or emulators.
- **Truthful Status Reporting**: UI badge explicitly distinguishes `● On-Device AI`, `● Cloud AI`, or `● Offline AI`.

---

## 3. Dual-Channel Collaboration Resilience

```
               STUDENT PHONE (iQOO)
                        │
         ┌──────────────┴──────────────┐
         ↓                             ↓
WebSocket Connection          REST Polling Fallback
   (/api/collaboration/ws)       (/api/collaboration/*)
         │                             │
         └──────────────┬──────────────┘
                        ↓
             TEACHER LAPTOP DASHBOARD
```

- If WebSocket disconnects, mobile client automatically falls back to REST polling every 3 seconds to fetch pending teacher actions (`START_REVISION`) and acknowledge completion.

---

## 4. Fallback Execution Matrix

| Trigger Event | Fallback Path | Behavioral Result |
| :--- | :--- | :--- |
| **Gemini API Offline** | `GeminiProvider` -> `FallbackProvider` | AI Tutor returns structured educational explanation without crashing. |
| **Network Disconnect** | Cloud AI -> Deterministic Knowledge Base | Offline knowledge engine handles prompts locally. |
| **Voice Speech Failure** | Speech Service State Machine | Switches gracefully from listening to deterministic speech response. |
| **Vision Model Offline** | `GeminiVisionProvider` -> `LocalOcrProvider` | Local OCR extracts question text for manual confirmation. |

---

## 5. Double Demo Reset Rehearsal Results

Executed `POST /api/teacher/demo/reset` across two consecutive demo cycles:
- **Cycle 1**: Dispatched custom revision activity -> Issued reset -> Baseline metrics (42 students, 78% average score, 0 activities) restored.
- **Cycle 2**: Repeated full demo flow -> Issued reset -> Baseline metrics restored identically without state corruption or stale event leaks.
