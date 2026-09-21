# LEARNsync AI — Deep AI Tutor Diagnostic and Fix Report

## Diagnostic Summary

### ROOT CAUSE
1. **Gemini Model 404 Error**: `GEMINI_MODEL` was configured as `gemini-2.5-flash` in `backend/.env` and `config.py`. The Google `google-genai` SDK returned `ClientError: 404 NOT_FOUND` for model `models/gemini-2.5-flash`.
2. **Multi-Turn Role Formatting Error**: `GeminiProvider._build_alternating_contents` generated consecutive `user` role entries when appending past history messages. Google Gemini API requires strictly alternating roles (`user` -> `model` -> `user` -> `model`), resulting in `ClientError: 400 Bad Request`.
3. **Frontend Missing Conversation ID**: `StudentWebAppView.jsx` sent chat requests without a `conversation_id`, causing backend multi-turn context lookups to fall back to a generic default session buffer.
4. **Client-Side Fallback Overwrite**: `StudentWebAppView.jsx` had a `catch` block that called `generateClientFallback()` which replaced backend responses with hardcoded text.

### FIX
1. **Updated Model Configuration**: Changed `GEMINI_MODEL` to `gemini-3.5-flash-lite` in `backend/.env`, `backend/.env.example`, and `backend/app/core/config.py`.
2. **Strict Alternating Role Builder**: Updated `GeminiProvider._build_alternating_contents` to merge consecutive user/model turns into single messages with newline separation, maintaining valid `user` <-> `model` turn sequencing for `google-genai` SDK.
3. **Frontend Conversation Tracking**: Added persistent state `conversationId` in `StudentWebAppView.jsx` and passed `conversation_id` in `POST /api/tutor/chat` JSON payload.
4. **Direct API Response Rendering**: Removed client-side fallback overwriting in `StudentWebAppView.jsx` so actual Gemini API output is rendered directly to the student UI.

---

## Test Metric Matrix

- **PROVIDER USED**: GeminiProvider
- **REAL GEMINI REQUEST**: PASS
- **GEMINI RESPONSE RECEIVED**: PASS
- **FRONTEND RECEIVED SAME RESPONSE**: PASS
- **MULTI-TURN**: PASS
- **SIMPLE MODE**: PASS
- **REAL_WORLD MODE**: PASS
- **TECHNICAL MODE**: PASS
- **C FUNDAMENTALS**: PASS
- **JAVA INHERITANCE**: PASS
- **ML OVERFITTING**: PASS
- **BINARY SEARCH**: PASS
- **TCP VS UDP**: PASS
- **BACKEND TESTS**: 75/75
- **FRONTEND BUILD**: PASS

---

## Technical Trace

```
StudentWebAppView (React frontend)
    ↓ POST /api/tutor/chat { message, explanation_mode, conversation_id }
Tutor route (backend/app/routes/tutor.py)
    ↓ tutor_service.chat_response()
AIRouterService (backend/app/services/ai_router_service.py)
    ↓ router.get_provider("tutor") -> GeminiProvider
GeminiProvider (backend/app/providers/gemini_provider.py)
    ↓ client.models.generate_content(model="gemini-3.5-flash-lite", contents=[...])
google-genai SDK
    ↓ HTTP POST https://generativelanguage.googleapis.com
Google Gemini API
    ↓ 200 OK + Real Generated Content
Gemini response parsing
    ↓ ProviderResponse(text=..., metadata={provider: gemini, fallback_used: false})
FastAPI HTTP 200 JSON Response
    ↓ { answer: "...", provider_used: "gemini", fallback_used: false }
StudentWebAppView
    ↓ setState(messages -> renders Markdown answer)
Rendered AI message
```
