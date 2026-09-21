# LearnSync AI — Final Startup Guide

Simple, step-by-step instructions for team members and evaluators to launch the complete LearnSync AI platform.

---

## Prerequisites

1. **Python**: 3.10+ installed
2. **Node.js**: 18+ installed
3. **Flutter**: Installed for mobile testing (or use Android APK)
4. **Network**: Laptop and iQOO smartphone connected to the same Wi-Fi / Hotspot

---

## Step 1: Start Backend Server

```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Install dependencies:
pip install -r requirements.txt
# Launch server bound to 0.0.0.0 for LAN access:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify backend health: Open `http://localhost:8000/docs` or `http://localhost:8000/api/ai/status`.

---

## Step 2: Start Teacher Dashboard

```bash
cd teacher-dashboard
npm install
npm run dev
```

Open `http://localhost:5173` (or port shown in terminal) to view the Teacher Intelligence Dashboard.

---

## Step 3: Configure Laptop LAN IP for Mobile

1. Find your laptop's local IP address:
   - On Windows: `ipconfig` (e.g., `192.168.1.50`)
2. Update `lib/config/api_config.dart` in Flutter app if using physical device:
   ```dart
   static const String baseUrl = 'http://192.168.1.50:8000';
   ```

---

## Step 4: Launch Student Mobile App

```bash
# In project root:
flutter pub get
flutter run
```

Or install the compiled Android APK on the physical iQOO phone.

---

## Step 5: Reset Demo State

Click **Reset Demo** in the top right header of the Teacher Dashboard (or issue `POST http://localhost:8000/api/teacher/demo/reset`) to restore baseline hackathon demo data.
