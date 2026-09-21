# LearnSync AI — Connecting Every Learner to Smarter Learning

> **A general-purpose AI-powered education web platform connecting students, personalized learning intelligence, and teachers.**

LearnSync AI supports:
- desktop browsers
- laptop browsers
- tablet browsers
- mobile browsers

---

## 🌟 Overview

**LearnSync AI** is a general-purpose, AI-powered intelligent education web platform accessible from any desktop, laptop, tablet, or mobile browser. It connects every learner to personalized AI-powered tutoring, multimodal question solving, and adaptive assessments, while giving teachers real-time classroom analytics, misconception detection, and one-tap targeted revision dispatch.

```
                LEARNSYNC AI WEB PLATFORM
                           │
             ┌─────────────┴─────────────┐
             │                           │
      STUDENT WEB APP             TEACHER WEB APP
   (Desktop / Tablet / Mobile)     (Dashboard & Analytics)
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                    FASTAPI BACKEND
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
    AI Router       Learning Engine     Collaboration Engine
        │                  │                  │
 ┌──────┼──────┐           ▼                  ▼
 ▼      ▼      ▼    Learning Profile    Real-Time Sync
Local Gemini Fallback
 AI     Cloud   Engine
```

---

## ✨ Key Features

### 1. Multimodal Student AI Tutor
- **Text Dialogue**: Multi-turn educational conversations with **Simple**, **Real-World**, and **Technical** explanation modes.
- **Voice AI**: Browser-compatible speech recognition with real-time transcription and typed input fallbacks.
- **Camera & Vision AI**: Upload or capture problem images through any desktop or mobile browser, extract OCR text, confirm/edit, and receive instant step-by-step solutions.

### 2. Adaptive Learning Engine
- **Adaptive Assessment**: Real-time adaptive difficulty engine adjusting question challenge dynamically (Easy → Medium → Hard).
- **Learning Profile**: Calculates subject & overall mastery (0–100%), tracks historical vs. recent performance, flags repeated mistakes, and generates explainable recommendations.

### 3. Teacher Intelligence Dashboard
- **Classroom Intelligence**: Aggregates class performance metrics, score distributions, and struggling student counts.
- **Misconception Detection**: Identifies underlying student misconceptions (e.g. confusing waiting time vs. turnaround time in process scheduling).
- **Targeted Revision Push**: Teachers dispatch targeted revision activities directly to student web apps with one tap.

### 4. Real-Time Classroom Sync
- **Bi-Directional Collaboration**: Dual-channel WebSocket connection with REST polling fallback connecting student and teacher interfaces.
- **In-App Student Notification Banner**: Alert banners notify students when a teacher assigns revision activities, allowing instant quiz launch from any device.

### 5. Multi-Tier AI Provider Abstraction
- **Unified AI Router**: `AIRouterService` manages provider priorities: `Local Engine → Gemini Cloud → Offline Fallback`.
- **Truthful Provider Reporting**: Clean UI indicators display `● Local AI`, `● Cloud AI`, or `● Offline AI`.

---

## 🛠️ Technology Stack

- **Student Web Application**: Responsive Flutter / Web interface supporting Desktop, Tablet, and Mobile views.
- **Teacher Dashboard**: React 18, Vite, CSS, Lucide Icons, WebSockets + REST Polling Sync.
- **Backend Services**: FastAPI (Python 3.12), Pydantic v2, WebSockets, Asyncio, Pytest.

---

## 🚀 Quick Start Guide

### 1. Backend Server
```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation available at: `http://localhost:8000/docs`

### 2. Teacher Dashboard
```bash
cd teacher-dashboard
npm install
npm run dev
```
Dashboard available at: `http://localhost:5173`

### 3. Student Web App
```bash
flutter pub get
flutter run -d chrome
```

---

## 🔒 Security & Privacy

- Backend credentials (`GEMINI_API_KEY`) remain strictly in `backend/.env`.
- Zero API keys exposed in frontend web builds or student app bundles.
- `/api/ai/status` exposes capability status flags without disclosing credentials.
- Uploaded vision images are processed in-memory and discarded immediately.

---

## 📊 Automated Verification

- **Backend Pytest Suite**: 69 passing unit/integration tests (`python -m pytest`).
- **Teacher Dashboard Production Build**: `npm run build` compiles clean with zero errors.

---

## 📱 Original Hackathon / Device Integration Context

> *Historical Note:* LearnSync AI was originally developed during an iQOO / Android hackathon environment. Native Kotlin bridge code (`DeviceCapabilityDetector.kt`, `LocalInferenceBridge.kt`) and Snapdragon NPU readiness paths exist as optional, platform-specific infrastructure for native Android hardware. The core LearnSync AI application runs seamlessly as a general-purpose web platform on any standard browser without hardware dependencies.
