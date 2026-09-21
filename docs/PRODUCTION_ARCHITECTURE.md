# LearnSync AI — Production Architecture Specification

## Overview
LearnSync AI is a general-purpose, AI-powered education web application designed for computer science and engineering students. The platform delivers personalized tutoring, multimodal vision problem solving, adaptive assessment challenges, real-time teacher analytics, and live collaboration.

---

## 1. System Architecture Diagram

```mermaid
graph TD
    Client[React/Vite Web App / Mobile Browser] -->|HTTPS REST| Proxy[Nginx / Cloudflare Ingress]
    Client -->|WSS WebSockets| Proxy
    
    Proxy -->|Reverse Proxy /api/*| Backend[FastAPI App Server (Uvicorn / Gunicorn)]
    
    Backend -->|Secret API Key| Gemini[Google Gemini GenAI Cloud API]
    Backend -->|BSON CRUD| Mongo[MongoDB Atlas Cluster]
    Backend -->|In-Memory Buffer| LocalNPU[Local AI / NPU Hardware Accelerator]
```

---

## 2. Component Boundaries & Responsibilities

### Frontend Layer (`teacher-dashboard`)
- **Framework**: React 18, Vite 5, Vanilla CSS Design Tokens.
- **API Client**: Centralized URL builder (`src/config/apiConfig.js`) using environment variables (`VITE_API_BASE_URL` & `VITE_WS_BASE_URL`) with relative `/api` fallback for local Vite dev proxying.
- **State & Error Handling**: Tabbed workspace views guarded by React `ErrorBoundary` wrappers. Zero raw API key exposure to browser memory or local storage.

### Backend Application Layer (`backend`)
- **Framework**: FastAPI (Python 3.12), ASGI Uvicorn workers.
- **Core Orchestrator**: `AIRouterService` dynamically routes requests:
  - Local/On-Device NPU $\rightarrow$ Gemini Cloud API $\rightarrow$ Offline Fallback Provider.
- **Providers**:
  - `GeminiProvider`: Multi-turn tutoring with retry & exponential backoff.
  - `GeminiAssessmentProvider`: Structured MCQ question generation (`gemini-3.5-flash-lite`).
  - `GeminiVisionProvider`: Multimodal image OCR & step-by-step solution breakdown (`gemini-3.5-flash-lite`).
  - `FallbackProvider`: Deterministic offline fallback ensuring zero downtime.

### Data & Real-Time Sync Layer
- **Persistence**: MongoDB Atlas for user learning profiles, assessment history, and student analytics.
- **WebSockets**: `/api/collaboration/ws/...` for real-time classroom events with automatic 4-second REST polling fallback.

---

## 3. Security Architecture
- **Secret Isolation**: `GEMINI_API_KEY` is loaded strictly from environment variables in backend `Settings`. Never exposed to frontend code or API responses.
- **CORS Protection**: Configurable `CORS_ORIGINS` restricting browser origins in production environments.
- **Upload Security**: 5 MB file size limit and strict MIME validation (`image/png`, `image/jpeg`, `image/jpg`, `image/webp`). Image payloads processed in-memory without persistent disk storage.
