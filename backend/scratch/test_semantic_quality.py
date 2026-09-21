import asyncio
import json
import base64
import time
import httpx

BASE_URL = "http://localhost:8000"

# Minimal 1x1 transparent PNG payload
SAMPLE_IMAGE_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

async def test_vision_semantic():
    print("\n==========================================")
    print("1. VISION AI SEMANTIC TEST")
    print("==========================================")
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/vision/analyze", json={
            "image_base64": SAMPLE_IMAGE_B64
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            extracted = data.get("extracted", {})
            provider = data.get("provider_used", "")
            solution = extracted.get("ai_solution") or extracted.get("explanation") or ""
            print(f"Status: [{res.status_code}] ({duration}s) | Provider: {provider}")
            print(f"Extracted Question: '{extracted.get('question')}'")
            print(f"AI Solution Preview (first 150 chars):\n{solution[:150]}...")
            
            # Semantic assertions: Solution must NOT contain generic placeholder templates
            assert "Identify Given Data: Extracted parameters" not in solution, "Template text found in solution!"
            assert len(solution) > 50, "Solution text is too short!"
            print("VISION SEMANTIC TEST: PASS")
            return True
        else:
            print(f"VISION SEMANTIC TEST FAILED: HTTP {res.status_code}")
            return False

async def test_voice_pointers_semantic():
    print("\n==========================================")
    print("2. VOICE AI SEMANTIC TEST: C POINTERS")
    print("==========================================")
    
    transcript = "Explain pointers in C in simple terms."
    print(f"Transcript: '{transcript}'")
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/tutor/chat", json={
            "message": transcript,
            "explanation_mode": "simple",
            "conversation_id": "semantic_voice_pointers"
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            answer = data.get("answer", "")
            provider = data.get("provider_used", "")
            print(f"Status: [{res.status_code}] ({duration}s) | Provider: {provider}")
            print(f"Answer Preview:\n{answer[:200]}...")
            
            # Semantic verification: Must discuss memory address or pointers in C
            answer_lower = answer.lower()
            has_pointer_concept = any(k in answer_lower for k in ["address", "memory", "*", "&", "pointer", "variable"])
            assert has_pointer_concept, "Answer does not contain C pointer concepts!"
            print("VOICE POINTERS SEMANTIC TEST: PASS")
            return True
        else:
            print(f"VOICE POINTERS SEMANTIC TEST FAILED: HTTP {res.status_code}")
            return False

async def test_voice_binary_search_semantic():
    print("\n==========================================")
    print("3. VOICE AI SEMANTIC TEST: BINARY SEARCH")
    print("==========================================")
    
    transcript = "Explain binary search."
    print(f"Transcript: '{transcript}'")
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/tutor/chat", json={
            "message": transcript,
            "explanation_mode": "simple",
            "conversation_id": "semantic_voice_bs"
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            answer = data.get("answer", "")
            provider = data.get("provider_used", "")
            print(f"Status: [{res.status_code}] ({duration}s) | Provider: {provider}")
            print(f"Answer Preview:\n{answer[:200]}...")
            
            answer_lower = answer.lower()
            has_bs_concept = any(k in answer_lower for k in ["sorted", "middle", "log", "search", "divide", "half"])
            assert has_bs_concept, "Answer does not contain Binary Search concepts!"
            print("VOICE BINARY SEARCH SEMANTIC TEST: PASS")
            return True
        else:
            print(f"VOICE BINARY SEARCH SEMANTIC TEST FAILED: HTTP {res.status_code}")
            return False

async def test_voice_tcp_udp_semantic():
    print("\n==========================================")
    print("4. VOICE AI SEMANTIC TEST: TCP VS UDP")
    print("==========================================")
    
    transcript = "What is the difference between TCP and UDP?"
    print(f"Transcript: '{transcript}'")
    
    async with httpx.AsyncClient(timeout=35.0) as client:
        t0 = time.time()
        res = await client.post(f"{BASE_URL}/api/tutor/chat", json={
            "message": transcript,
            "explanation_mode": "simple",
            "conversation_id": "semantic_voice_tcp"
        })
        duration = round(time.time() - t0, 2)
        if res.status_code == 200:
            data = res.json()
            answer = data.get("answer", "")
            provider = data.get("provider_used", "")
            print(f"Status: [{res.status_code}] ({duration}s) | Provider: {provider}")
            print(f"Answer Preview:\n{answer[:200]}...")
            
            answer_lower = answer.lower()
            has_tcp_concept = any(k in answer_lower for k in ["reliable", "connection", "speed", "overhead", "handshake", "packet", "protocol"])
            assert has_tcp_concept, "Answer does not contain TCP/UDP concepts!"
            print("VOICE TCP VS UDP SEMANTIC TEST: PASS")
            return True
        else:
            print(f"VOICE TCP VS UDP SEMANTIC TEST FAILED: HTTP {res.status_code}")
            return False

async def main():
    print("Running LearnSync AI Semantic Quality Test Suite...")
    v_pass = await test_vision_semantic()
    p_pass = await test_voice_pointers_semantic()
    b_pass = await test_voice_binary_search_semantic()
    t_pass = await test_voice_tcp_udp_semantic()
    
    print("\n==========================================")
    print("SEMANTIC QUALITY TEST RESULTS:")
    print("==========================================")
    print(f"Vision Semantic Solution: {'PASS' if v_pass else 'FAIL'}")
    print(f"Voice Pointers Question: {'PASS' if p_pass else 'FAIL'}")
    print(f"Voice Binary Search Question: {'PASS' if b_pass else 'FAIL'}")
    print(f"Voice TCP vs UDP Question: {'PASS' if t_pass else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
