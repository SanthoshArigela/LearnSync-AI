# LearnSync AI — Hackathon Presentation & Demonstration Guide

> **Historical Hackathon / Device Integration**  
> LearnSync AI is a general-purpose AI education web platform. The guide below documents historical hackathon device testing and physical hardware demonstration workflows.

---

## 🚀 Quick Start & Environment Verification

### 1. Start FastAPI Backend Server
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Health Check: `http://127.0.0.1:8000/api/health`
- Live OpenAPI Docs: `http://127.0.0.1:8000/docs`

### 2. Start Teacher Intelligence Dashboard (React + Vite)
```bash
cd teacher-dashboard
npm run dev
```
- Local URL: `http://127.0.0.1:5173`

### 3. Run Student Mobile Application (Flutter / iQOO Android)
```bash
flutter run -d chrome # Or run on physical iQOO Android device
```

---

## 🎬 10-Step Live Demonstration Script

| Step | Action | Feature Highlight |
|---|---|---|
| **1. Phone AI** | Student asks: *"Why does TCP use a three-way handshake?"* | Multi-turn AI Tutor with Simple / Real-World / Technical explanation modes |
| **2. Voice AI** | Student taps 🎙 icon and asks naturally by voice | Speech state machine (Listening → Processing → Transcribing → Tutor Handoff) |
| **3. Camera AI** | Student scans question: *"Solve: 2x + 5 = 15"* | Vision AI OCR + Step-by-Step mathematical reasoning handoff |
| **4. Adaptive Assessment** | Student completes 5-question Operating Systems Quiz | Live difficulty scaling & concept evaluation |
| **5. Learning Profile** | Student scores 58% on Process Scheduling | Automatic Learning Gap Detection (`Needs Attention: < 60%`) |
| **6. Real-Time Sync** | Event `ASSESSMENT_COMPLETED` sent over WebSocket | Phone ↔ Laptop real-time classroom collaboration loop |
| **7. Teacher Dashboard** | Dashboard live feed flashes: `Process Scheduling — 58% (17 Students Affected)` | Classroom intelligence, weak topic detection & misconception extraction |
| **8. AI Recommendation** | Dashboard displays explainable AI recommendation card | WHAT, WHO, WHY, ACTION, & EXPECTED GOAL rationale |
| **9. Teacher Action** | Teacher clicks `🚀 Create Revision Activity` → `Send to Students` | Real-time action dispatch with delivery confirmation (`✓ Delivered`) |
| **10. Closed Loop** | Student phone pops up banner: *"Teacher Revision Activity Received"* | Instant launch into 5-question targeted adaptive revision quiz |

---

## 🔄 Demo Reset & Failure Resilience
- **Reset Demo State**: Click `🔄 Reset Demo` in the Teacher Dashboard status bar or Profile screen to reset all student scores, events, and recommendations to the baseline demo dataset.
- **Offline / Network Fallback**: If Gemini API keys or network connections are unavailable, LearnSync AI automatically switches to local fallback providers so the live pitch **never crashes or freezes**.
