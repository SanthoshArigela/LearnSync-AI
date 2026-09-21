# LearnSync AI — Hackathon Backup & Fallback Plan

## Contingency Matrix for Live Presentation

---

### Scenario 1: Wi-Fi / Internet Disconnects During Presentation
- **Impact**: Gemini Cloud API and external network calls fail.
- **Automated Fallback**: `AIRouterService` switches seamlessly to `FallbackProvider` (Deterministic Offline Knowledge Base).
- **Presentation Strategy**: Continue the demonstration normally. Highlight to judges: *"Even with Wi-Fi disconnected, LearnSync AI's offline fallback engine delivers structured educational explanations without interruption."*

---

### Scenario 2: WebSocket Connection Drops
- **Impact**: Real-time push events between phone and laptop are delayed.
- **Automated Fallback**: Mobile app switches automatically to REST polling fallback (`/api/collaboration/events` and `/api/collaboration/actions/student/*`) every 3 seconds.
- **Presentation Strategy**: The student phone receives the teacher revision activity banner within 3 seconds via REST polling fallback.

---

### Scenario 3: Physical Device Display Output Issues
- **Impact**: Projector cannot mirror physical smartphone screen.
- **Automated Fallback**: Launch Flutter web / desktop build or emulator instance on the laptop.
- **Presentation Strategy**: Run phone app and teacher dashboard side-by-side on the laptop display.

---

### Scenario 4: Stale Data / Interrupted Demo Flow
- **Impact**: Demo state gets out of sync during setup.
- **Automated Recovery**: Click **Reset Demo** button in the top-right header of the Teacher Dashboard (or execute `POST http://localhost:8000/api/teacher/demo/reset`).
- **Presentation Strategy**: Baseline metrics (42 students, 78% average score, 0 activities) restore cleanly in <100ms.
