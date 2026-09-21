# Sprint 9 — LearnSync AI Local AI & On-Device Intelligence Readiness

> *"LearnSync AI is designed so intelligence can move closer to the learner—from cloud AI to local/open-source models and eventually on-device/NPU inference—without changing the learning experience."*

---

## 🏗 System Architecture & AI Router Flow

```
                                  Student iQOO Phone
                                          │
                                          ▼
                                AIRouterService (backend)
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         │                                │                                │
         ▼                                ▼                                ▼
  LocalAIProvider                 GeminiProvider                   FallbackProvider
  (Snapdragon NPU Ready)          (Cloud Gemini 2.5)               (Structured Knowledge Base)
         │                                │                                │
         └────────────────────────────────┴────────────────────────────────┘
                                          │
                                          ▼
                         Unified Educational JSON Response
```

---

## ⚙️ AI Routing Behavior & Preference Order

LearnSync AI uses centralized, configurable AI Routing (`AI_PROVIDER_MODE=auto`).

### **Preference Order**:
1. **LOCAL AI**: Snapdragon NPU / LiteRT / llama.cpp on-device open-source SLM when available.
2. **CLOUD AI**: Gemini 2.5 Flash via backend API provider abstraction when local AI is uninstalled or busy.
3. **OFFLINE FALLBACK**: Zero-downtime deterministic structured knowledge base when both local and cloud AI are unavailable.

---

## 📡 Provider Status API (`/api/ai/status`)

Exposes active AI capability matrix and health metrics without leaking secrets:

```json
{
  "active_provider": "gemini",
  "active_model": "gemini-2.5-flash",
  "local_available": false,
  "gemini_available": true,
  "fallback_available": true,
  "mode": "auto",
  "offline_ready": true,
  "capabilities": {
    "supports_chat": true,
    "supports_vision": true,
    "supports_assessment": true,
    "supports_offline": true
  }
}
```

---

## 📱 On-Device NPU / Snapdragon Readiness Path

The `LocalAIProvider` capability interface defines standard properties for future hardware acceleration:
- `supports_chat`: `True`
- `supports_vision`: `True`
- `supports_assessment`: `True`
- `supports_offline`: `True`
- `is_available`: Dynamic availability check
- `model_name`: `"LearnSync-SLM-1.5B (Snapdragon NPU Ready)"`

---

## 🛡️ Security Audit
- **Zero API Key Leakage**: Gemini API keys exist exclusively inside backend `.env`. No keys in Flutter or React code.
- **Fail-Safe Offline Recovery**: If network drops or external API limits trigger, the system transitions to offline fallback without raising unhandled exceptions.
