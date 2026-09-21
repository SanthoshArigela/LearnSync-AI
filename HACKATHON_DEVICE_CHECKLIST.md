# LearnSync AI — Hackathon Physical Device & Demo Checklist

> **Historical Hackathon / Device Integration**  
> *Note: This checklist documents historical physical device testing workflows.*

## PRE-DEMO SETUP

- [x] Laptop charged.
- [x] iQOO smartphone charged.
- [x] Backend server running on `0.0.0.0:8000`.
- [x] Teacher Dashboard running on port 5173 / 3000.
- [x] Flutter app installed on iQOO smartphone.
- [x] Laptop and iQOO phone connected to same Wi-Fi / Hotspot network.
- [x] Laptop LAN IP verified (e.g. `192.168.1.50`).
- [x] `lib/config/api_config.dart` configured with laptop IP address.
- [x] Camera permission granted on phone.
- [x] Microphone permission granted on phone.
- [x] One-tap **Reset Demo** executed on Teacher Dashboard.

---

## LIVE DEMO REHEARSAL TRAJECTORY (15 STEPS)

1. **Student Ask**: Open AI Tutor -> Ask *"Why does TCP use a three-way handshake?"*
2. **Concept Delivery**: Show Concept Summary, Simple Explanation, Real-world Example, Key Takeaway.
3. **Voice AI**: Tap Mic -> Speak concept -> Show Listening -> Transcribing -> Response.
4. **Camera Vision AI**: Tap Camera -> Scan problem *"Solve 2x + 5 = 15"* -> Tap Analyze -> View solution.
5. **Adaptive Assessment**: Open Assess -> Start Operating Systems quiz -> Answer 5 questions adaptively.
6. **Weak Topic Detected**: View result -> Detect *Process Scheduling (58%)*.
7. **Learning Profile Updated**: Show updated topic mastery score.
8. **Teacher Dashboard Live Sync**: Switch to laptop -> Show live feed event *Santhosh K. — Process Scheduling (58%)*.
9. **Targeted Revision Action**: Click **Create Revision Activity** -> Dispatch to student.
10. **Student In-App Banner**: Show top banner on phone *"Teacher Revision Activity Received"* -> Tap **Start Revision** -> Launch targeted quiz.
11. **Targeted Practice Completed**: Complete 5-question targeted quiz.
12. **Progress Reflected**: Show updated student learning profile and teacher analytics.
13. **Reset Demo Cycle 1**: Click **Reset Demo** -> Confirm baseline data restored.
14. **Reset Demo Cycle 2**: Issue reset again -> Confirm state restoration is 100% repeatable.
15. **Fallback Safety**: Verify offline knowledge base / REST polling fallback if Wi-Fi drops.

---

## BACKUP / FAIL-SAFE PROCEDURES

- **Network Interruption**: AI Router switches seamlessly to deterministic fallback.
- **WebSocket Disconnect**: REST polling fallback maintains sync automatically.
- **Demo State Recovery**: One-tap **Reset Demo** instantly restores clean baseline state.
