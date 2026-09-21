# LearnSync AI — Final Hackathon Demo Checklist

> **Historical Hackathon / Device Integration**  
> *Note: This checklist documents historical hackathon demo setup procedures.*

## Pre-Demo Preparation (5 Minutes Before Pitch)

- [ ] **Backend Server**: Ensure FastAPI backend is running on host `0.0.0.0:8000`.
  ```bash
  cd backend
  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
- [ ] **Teacher Dashboard**: Ensure React dashboard is running on port 3000/5173.
  ```bash
  cd teacher-dashboard
  npm run dev
  ```
- [ ] **iQOO Smartphone Connection**: Connect iQOO phone and teacher laptop to the same Wi-Fi / Hotspot network.
- [ ] **Backend IP Config**: Update `lib/config/api_config.dart` with the laptop's LAN IP address (e.g., `192.168.1.50:8000`).
- [ ] **Permissions**: Grant Camera and Microphone permissions on the Android phone.
- [ ] **Reset Demo State**: Click **Reset Demo** in the Teacher Dashboard header to restore baseline data.

---

## Live Demonstration Steps

1. **AI Tutor Query**:
   - Open AI Tutor on phone.
   - Ask: *"Why does TCP use a three-way handshake?"*
   - Show Concept Summary, Simple Explanation, Real-world Example, and Follow-up chips.

2. **Voice AI Mode**:
   - Tap Mic icon.
   - Speak: *"Explain TCP three-way handshake."*
   - Demonstrate Listening -> Transcribing -> Response.

3. **Camera Vision AI**:
   - Tap Camera icon.
   - Scan problem: *"Solve 2x + 5 = 15"*.
   - Tap **Analyze Question** -> Show step-by-step solution.

4. **Adaptive Assessment**:
   - Open **Assess** tab -> Start **Operating Systems** assessment.
   - Answer 5 questions adaptively.
   - Complete assessment -> View score, Strong Topics, and Weak Topic (*Process Scheduling 58%*).

5. **Teacher Dashboard Real-Time Sync**:
   - Switch focus to Laptop Teacher Dashboard.
   - Point out **Live Classroom Feed** showing real-time event: *Santhosh K. — Process Scheduling (58%)*.

6. **Targeted Revision Push**:
   - Click **Create Revision Activity** for *Process Scheduling*.
   - Click **Send Activity to Phone**.

7. **Student Notification & Quiz Launch**:
   - Show student phone receiving top banner: *"Your teacher sent you a revision activity"*.
   - Tap **Start Revision** -> Launch targeted adaptive quiz.

8. **AI Status & NPU Pill**:
   - Highlight AppBar badge showing active provider mode (`On-Device AI`, `Cloud AI`, or `Offline AI`).

---

## Backup / Fail-Safe Procedures

- **Offline Mode**: If Wi-Fi breaks during presentation, AI Router automatically switches to `FallbackProvider` (Offline Knowledge Base) and REST polling fallback seamlessly.
- **Demo Reset**: Click **Reset Demo** anytime to recover from an unexpected demo state.
