# LearnSync AI — Final Hackathon Pitch Guide

> **Historical Hackathon / Device Integration**  
> *Note: This pitch guide reflects historical hackathon presentation materials.*

## Pitch Overview (3–5 Minute Presentation Track)

---

### 1. The Problem (30 Seconds)
"Today, students use AI tools to solve homework, but learning stays trapped inside the student's screen. Teachers have no visibility into *where* individual students struggle, leading to unaddressed misconceptions and learning gaps."

---

### 2. The Solution (45 Seconds)
"Introducing **LearnSync AI — Connecting Every Learner to Smarter Learning**. LearnSync AI turns the student's iQOO smartphone into a hyper-personalized multimodal learning companion and connects real-time classroom learning intelligence to the teacher's laptop dashboard."

---

### 3. Student Mobile Experience (1 Minute 15 Seconds)
- **AI Tutor**: Instant explanation in Simple, Real-World, or Technical modes.
- **Voice AI**: Hands-free natural speech interaction.
- **Camera Vision AI**: Snap homework questions, extract OCR text, and generate step-by-step guidance.
- **Adaptive Assessment**: Dynamic difficulty adjustment evaluating true concept mastery.

---

### 4. Teacher Intelligence & Office Kit Collaboration (1 Minute)
- **Live Classroom Feed**: As students take assessments on their iQOO phones, weak topics and misconceptions sync live to the teacher dashboard over local Wi-Fi/LAN.
- **Targeted Revision**: The teacher sees that 17 students are struggling with *Process Scheduling* and pushes a 10-minute targeted revision activity directly back to their phones with one tap.
- **Student Action**: The student taps "Start Revision" and completes a targeted adaptive quiz.

---

### 5. On-Device Snapdragon NPU AI Architecture (45 Seconds)
- **Smart Routing**: Unified `AIRouterService` routes prompts intelligently: **On-Device NPU -> Gemini Cloud AI -> Deterministic Offline Fallback**.
- **Offline Readiness**: If Wi-Fi drops, LearnSync AI continues working seamlessly using local educational models and knowledge bases.
- **On-Device Capabilities**: Native Kotlin MethodChannel bridge detects Snapdragon Hexagon NPU hardware capabilities.

---

### 6. Closing Statement (15 Seconds)
"LearnSync AI doesn't just answer what a student asks. It understands where the student struggles and connects that insight to the teacher so the entire classroom can learn better."
