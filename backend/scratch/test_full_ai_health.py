import asyncio
import json
import base64
import time
import httpx

BASE_URL = "http://localhost:8000"

# Minimal 1x1 transparent PNG as base64 for Vision test
SAMPLE_IMAGE_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

async def test_tutor():
    print("\n==========================================")
    print("TESTING 1: AI TUTOR (/api/tutor/chat)")
    print("==========================================")
    
    questions = [
        "What are the fundamentals of C programming?",
        "Explain pointers in C.",
        "Give me a simple pointer example.",
        "What is overfitting in machine learning?",
        "Explain TCP vs UDP."
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        conv_id = "health_test_conv"
        # Reset conversation first
        await client.post(f"{BASE_URL}/api/tutor/reset?conversation_id={conv_id}")
        
        for i, q in enumerate(questions, 1):
            t0 = time.time()
            res = await client.post(f"{BASE_URL}/api/tutor/chat", json={
                "message": q,
                "explanation_mode": "simple",
                "conversation_id": conv_id
            })
            duration = round(time.time() - t0, 2)
            if res.status_code == 200:
                data = res.json()
                provider = data.get("provider_used", "unknown")
                fallback = data.get("fallback_used", False)
                topic = data.get("topic", "N/A")
                print(f"Request {i}: [{res.status_code}] ({duration}s) | Provider: {provider} | Fallback: {fallback} | Topic: {topic}")
                assert fallback == False, f"Fallback used on request {i}"
            else:
                print(f"Request {i} FAILED with status {res.status_code}: {res.text}")
                return False
    return True

async def test_assessment():
    print("\n==========================================")
    print("TESTING 2: ADAPTIVE ASSESSMENT (/api/assessment/generate)")
    print("==========================================")
    
    subjects = [
        ("Computer Science", "Computer Networks", "medium"),
        ("Computer Science", "DBMS", "easy"),
        ("Computer Science", "Operating Systems", "hard")
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for subj, topic, diff in subjects:
            t0 = time.time()
            res = await client.post(f"{BASE_URL}/api/assessment/generate", json={
                "subject": subj,
                "topic": topic,
                "difficulty": diff,
                "question_count": 3
            })
            duration = round(time.time() - t0, 2)
            if res.status_code == 200:
                data = res.json()
                questions = data.get("questions", [])
                provider = data.get("provider_used", "unknown")
                print(f"Generate [{topic}]: [{res.status_code}] ({duration}s) | Provider: {provider} | Questions: {len(questions)}")
                if questions:
                    print(f"  Q1: {questions[0].get('question', '')[:60]}...")
                    print(f"  Options: {len(questions[0].get('options', []))} options")
                assert len(questions) > 0, "No questions generated"
            else:
                print(f"Generate [{topic}] FAILED with status {res.status_code}: {res.text}")
                return False
    return True

async def test_vision():
    print("\n==========================================")
    print("TESTING 3: VISION AI (/api/vision/analyze)")
    print("==========================================")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/vision/analyze", json={
            "image_base64": SAMPLE_IMAGE_B64
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            success = data.get("success", False)
            provider = data.get("provider_used", "unknown")
            extracted = data.get("extracted", {})
            print(f"Vision analyze: [{res.status_code}] ({duration}s) | Success: {success} | Provider: {provider}")
            print(f"  Extracted Question: {extracted.get('question', '')}")
            print(f"  Topic: {extracted.get('topic', '')}")
            return success
        else:
            print(f"Vision analyze FAILED with status {res.status_code}: {res.text}")
            return False

async def test_voice():
    print("\n==========================================")
    print("TESTING 4: VOICE AI (Transcript -> Tutor Chat Flow)")
    print("==========================================")
    
    # Voice AI flow: Microphone -> Transcript -> POST /api/tutor/chat -> Gemini -> Voice UI
    transcript = "Explain binary search."
    print(f"Simulating microphone transcript: '{transcript}'")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/tutor/chat", json={
            "message": transcript,
            "explanation_mode": "simple",
            "conversation_id": "voice_test_conv"
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            provider = data.get("provider_used", "unknown")
            fallback = data.get("fallback_used", False)
            answer = data.get("answer", "")
            print(f"Voice Request: [{res.status_code}] ({duration}s) | Provider: {provider} | Fallback: {fallback}")
            print(f"  Answer preview: {answer[:80]}...")
            assert fallback == False, "Voice request fell back"
            return True
        else:
            print(f"Voice Request FAILED with status {res.status_code}: {res.text}")
            return False

async def test_stability_10_ops():
    print("\n==========================================")
    print("TESTING 5: 10-OPERATION STABILITY MIXED TEST")
    print("==========================================")
    
    ops = [
        ("tutor", {"message": "Explain queue data structure", "explanation_mode": "simple"}),
        ("assessment", {"subject": "Computer Science", "topic": "Data Structures", "difficulty": "medium", "question_count": 2}),
        ("vision", {"image_base64": SAMPLE_IMAGE_B64}),
        ("tutor", {"message": "What is bubble sort time complexity?", "explanation_mode": "technical"}),
        ("tutor", {"message": "Explain recursion with an example", "explanation_mode": "simple"}),
        ("assessment", {"subject": "Computer Science", "topic": "Algorithms", "difficulty": "hard", "question_count": 2}),
        ("vision", {"image_base64": SAMPLE_IMAGE_B64}),
        ("tutor", {"message": "What is dynamic programming?", "explanation_mode": "real-world"}),
        ("assessment", {"subject": "Computer Science", "topic": "Operating Systems", "difficulty": "easy", "question_count": 2}),
        ("tutor", {"message": "Explain deadlocks in OS", "explanation_mode": "simple"})
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        success_count = 0
        for i, (op_type, payload) in enumerate(ops, 1):
            t0 = time.time()
            if op_type == "tutor":
                res = await client.post(f"{BASE_URL}/api/tutor/chat", json=payload)
            elif op_type == "assessment":
                res = await client.post(f"{BASE_URL}/api/assessment/generate", json=payload)
            elif op_type == "vision":
                res = await client.post(f"{BASE_URL}/api/vision/analyze", json=payload)
            
            duration = round(time.time() - t0, 2)
            if res.status_code == 200:
                success_count += 1
                print(f"Op {i:02d} [{op_type.upper()}]: PASS ({duration}s)")
            else:
                print(f"Op {i:02d} [{op_type.upper()}]: FAIL [{res.status_code}] ({duration}s)")
        
        print(f"\n10-Operation Stability Summary: {success_count}/10 Passed")
        return success_count == 10

async def main():
    print("Starting LearnSync AI Full Health Diagnostic Test...")
    tutor_pass = await test_tutor()
    assess_pass = await test_assessment()
    vision_pass = await test_vision()
    voice_pass = await test_voice()
    stability_pass = await test_stability_10_ops()
    
    print("\n==========================================")
    print("FINAL TEST RESULTS SUMMARY:")
    print("==========================================")
    print(f"TUTOR: {'PASS' if tutor_pass else 'FAIL'}")
    print(f"ASSESSMENT: {'PASS' if assess_pass else 'FAIL'}")
    print(f"VISION: {'PASS' if vision_pass else 'FAIL'}")
    print(f"VOICE: {'PASS' if voice_pass else 'FAIL'}")
    print(f"10-OP STABILITY: {'PASS' if stability_pass else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
