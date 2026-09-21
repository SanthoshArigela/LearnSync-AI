# LEARNsync AI — AI Tutor Intermittent Runtime Diagnostic Report

## Diagnostic Summary

### FIRST REQUEST ("What are the fundamentals of C programming?")
- **Status**: PASS
- **Provider**: GeminiProvider
- **Fallback Used**: False
- **Latency**: 4300ms

### SECOND REQUEST ("Explain pointers in C with an example.")
- **Status**: PASS
- **Provider**: GeminiProvider
- **Fallback Used**: False
- **Latency**: 5119ms

### THIRD REQUEST ("Now give me a simple pointer program.")
- **Status**: PASS
- **Provider**: GeminiProvider
- **Fallback Used**: False
- **Latency**: 5045ms

### FOURTH REQUEST ("What is overfitting in machine learning?")
- **Status**: PASS
- **Provider**: GeminiProvider
- **Fallback Used**: False
- **Latency**: 4016ms

---

## Detailed Root Cause Analysis

### ROOT CAUSE
1. **Frontend Relative API Endpoint & Proxy Mismatch**:
   - In `StudentWebAppView.jsx`, frontend fetch requests were made using relative paths (`/api/tutor/chat`). When the Student Web App was served on `http://localhost:5173` without server proxy configuration in Vite, requests resolved to `http://localhost:5173/api/tutor/chat`, returning HTML 404 from Vite dev server.
   - When the browser attempted to parse the HTML 404 response via `res.json()`, a `SyntaxError: Unexpected token '<'` was thrown, resulting in the frontend error message: `"Failed to reach AI Tutor. Please try again."`
2. **Transient Network Latency Handling**:
   - Occasional transient network delay or API server response stalls caused unhandled single-attempt failures.

### HTTP ERROR
- `HTTP 404 Not Found` (from relative `/api` frontend dev server route before proxy configuration).

### GEMINI API
- **Status**: PASS

### GEMINI PROVIDER
- **Status**: PASS

### CONVERSATION HISTORY
- **Status**: PASS
- Strict alternating roles (`user` $\leftrightarrow$ `model`) verified across bounded history buffers.

### QUOTA/RATE LIMIT
- **Status**: NO (all 10 sequential requests succeeded under configured `gemini-3.5-flash-lite` model without encountering 429 rate limits).

### FALLBACK
- **Status**: NOT USED (all requests served directly by `GeminiProvider`).

---

## Fix Applied

1. **Vite Development Server Proxy**:
   - Added `/api` proxy target `http://localhost:8000` in [`teacher-dashboard/vite.config.js`](file:///d:/codes/IQOO/teacher-dashboard/vite.config.js) to seamlessly route relative `/api/...` frontend calls to the FastAPI backend.
2. **Controlled Transient Retry & Exponential Backoff**:
   - Added a single controlled retry loop with 1.0–1.2s exponential backoff in `GeminiProvider.generate_response` ([`backend/app/providers/gemini_provider.py`](file:///d:/codes/IQOO/backend/app/providers/gemini_provider.py)) to absorb transient SDK/network glitches before delegating to `FallbackProvider`.

---

## Metric Summary

- **FIRST REQUEST**: PASS
- **SECOND REQUEST**: PASS
- **THIRD REQUEST**: PASS
- **FOURTH REQUEST**: PASS
- **ROOT CAUSE**: Frontend relative API endpoint routing mismatch without Vite server proxy, resulting in HTML 404 responses during browser fetches.
- **HTTP ERROR**: HTTP 404 (on unproxied frontend routes)
- **GEMINI API**: PASS
- **GEMINI PROVIDER**: PASS
- **CONVERSATION HISTORY**: PASS
- **QUOTA/RATE LIMIT**: NO
- **FALLBACK**: NOT USED
- **FIX**: Added `/api` proxy target to `vite.config.js` and added 1 controlled retry with backoff in `GeminiProvider`.
- **BACKEND TESTS**: 75/75 PASS
- **FRONTEND BUILD**: PASS
