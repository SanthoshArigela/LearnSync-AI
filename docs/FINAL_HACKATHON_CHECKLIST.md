# LearnSync AI — Final Hackathon Presentation Checklist

> **Historical Hackathon / Device Integration**  
> *Note: This document reflects historical hackathon presentation materials.*

## BEFORE THE EVENT

- [x] Repository clean & `.gitignore` excluding secrets.
- [x] `.env` configured with Gemini API key (optional; fallback engine active if absent).
- [x] Backend runs cleanly on `0.0.0.0:8000`.
- [x] Teacher Dashboard builds cleanly (`npm run build`).
- [x] Flutter app analyzed (`flutter analyze`).
- [x] Camera & Microphone permissions added to `AndroidManifest.xml`.
- [x] Laptop & iQOO phone connected to same Wi-Fi.

---

## 5 MINUTES BEFORE PITCH

- [ ] Launch backend (`python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`).
- [ ] Launch teacher dashboard (`npm run dev`).
- [ ] Connect iQOO phone to app / backend.
- [ ] Click **Reset Demo** in Teacher Dashboard header.
- [ ] Confirm active provider badge shows `● On-Device AI`, `● Cloud AI`, or `● Offline AI`.

---

## LIVE DEMO SEQUENCE (23-STEP PATH)

1. **Student Ask**: Open AI Tutor -> Ask *"Why does TCP use a three-way handshake?"*
2. **Concept Delivery**: Show Concept Summary, Simple Explanation, Real-world Example, Key Takeaway.
3. **Voice AI**: Tap Mic -> Speak concept -> Show Listening -> Transcribing -> Response.
4. **Camera Vision AI**: Tap Camera -> Scan problem *"Solve 2x + 5 = 15"* -> Tap Analyze -> View solution.
5. **Adaptive Assessment**: Open Assess -> Start Operating Systems quiz -> Answer 5 questions adaptively.
6. **Weak Topic Detected**: View result -> Detect *Process Scheduling (58%)*.
7. **Learning Profile Updated**: Show updated topic mastery.
8. **Teacher Dashboard Live Sync**: Switch to laptop -> Show live feed event *Santhosh K. — Process Scheduling (58%)*.
9. **Targeted Revision Action**: Click **Create Revision Activity** -> Dispatch to student.
10. **Student In-App Banner**: Show top banner on phone *"Teacher Revision Activity Received"* -> Tap **Start Revision** -> Launch targeted quiz.
11. **Reset Demo**: Click **Reset Demo** to return state to baseline.

---

## BACKUP / FAIL-SAFE PROCEDURES

- **Network Offline**: AI Router switches seamlessly to deterministic fallback.
- **WebSocket Reconnect**: REST polling fallback maintains sync automatically if sockets disconnect.
- **Demo State Recovery**: One-tap **Reset Demo** instantly restores clean baseline state.
