# Google Gemini API Integration Documentation

## Overview
This document describes the integration of the official **Google Gemini API** (`google-genai` SDK v2.24.0) into **LearnSync AI** as the primary cloud AI provider for tutoring, multimodal vision analysis, and adaptive assessment generation.

---

## 1. Architecture Flow

```
Student Web App / Frontend
          │
          ▼
FastAPI Backend (/api/tutor/chat, /api/vision/analyze, /api/assessment/generate)
          │
          ▼
    AIRouterService
          │
  ┌───────┴────────┬─────────────────────┐
  │ (Mode: AUTO)   │                     │
  ▼                ▼                     ▼
GeminiProvider  LocalAIProvider     FallbackProvider
(Cloud GenAI)   (On-Device SLM/NPU) (Deterministic)
  │
  ▼
Google Gemini API (google-genai SDK)
```

---

## 2. Gemini Provider Implementation

- File: [`backend/app/providers/gemini_provider.py`](file:///d:/codes/IQOO/backend/app/providers/gemini_provider.py)
- Uses official SDK: `from google import genai`
- Instantiates `genai.Client(api_key=api_key)`
- Supports mode-adaptive educational prompt instructions, bounded multi-turn conversation context, and structured JSON parsing.

---

## 3. API Key & Model Configuration

Backend Configuration File: [`backend/app/core/config.py`](file:///d:/codes/IQOO/backend/app/core/config.py)

Environment Variables (`backend/.env`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
AI_PROVIDER_MODE=auto
```

Template File: [`backend/.env.example`](file:///d:/codes/IQOO/backend/.env.example)

---

## 4. Educational System Prompt

Gemini is configured with an educational system prompt:
- **Pedagogical Goal**: Teach principles and build intuition over giving raw answers.
- **Adaptive Level**: Automatically adapts terminology and depth based on student context.
- **Structure**: Markdown headers (`### Concept Summary`, `### Simple Explanation`, `### Real-World Example`, `### Key Takeaway`).
- **Code & Logic**: Explains logic line-by-line with code blocks, time/space complexity, and common pitfall warnings.

---

## 5. Explanation Modes

1. `SIMPLE`: Beginner-friendly, step-by-step, minimal jargon.
2. `REAL-WORLD`: Intuitive everyday analogies, real-life systems, practical technology scenarios.
3. `TECHNICAL`: Precise B.Tech CSE terminology, RFC protocols, memory layouts, algorithms, and code.

---

## 6. Multi-Turn Conversation Context

- Maintained via a bounded window of the last 10 messages.
- Formatted using `google.genai.types.Content(role=..., parts=[...])`.
- Enables contextual follow-up questions ("Why does it need a three-way handshake?").

---

## 7. Multimodal Vision Integration

- File: [`backend/app/providers/gemini_vision_provider.py`](file:///d:/codes/IQOO/backend/app/providers/gemini_vision_provider.py)
- Accepts base64 encoded images (PNG/JPEG/WebP).
- Converts to `types.Part.from_bytes(data=image_bytes, mime_type=mime_type)`.
- Extracts question text, topic, content type, and confidence metrics.

---

## 8. Adaptive Assessment Provider

- File: [`backend/app/providers/gemini_assessment_provider.py`](file:///d:/codes/IQOO/backend/app/providers/gemini_assessment_provider.py)
- Generates structured MCQ questions matching requested subject, topic, and difficulty.

---

## 9. Error Handling & Fallback Architecture

- **Missing/Invalid API Key**: Logs clean info message (never exposing keys) and delegates seamlessly to `FallbackProvider`.
- **API Timeout / Service Exception**: Catches exceptions gracefully and routes to `FallbackProvider` or returns clean user-facing error message without Python tracebacks.
- Router modes supported: `AUTO`, `GEMINI`, `LOCAL`, `FALLBACK`.

---

## 10. Security Verification

- API key is **never** sent to frontend client, browser JS, or API status endpoints.
- `GET /api/ai/status` exposes provider availability and model names while sanitizing keys and authorization headers.
- `.gitignore` protects `.env` files while tracking `.env.example`.

---

## 11. Local Setup Instructions

1. Copy environment template:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Edit `backend/.env` and set your real API key:
   ```env
   GEMINI_API_KEY=AIzaSy...
   GEMINI_MODEL=gemini-2.5-flash
   ```
3. Start backend server:
   ```bash
   cd backend
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
