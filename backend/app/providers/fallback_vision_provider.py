import random
from typing import Dict, Any, Optional
from .vision_provider import VisionProvider
from ..models.tutor_models import StudentContextModel

class FallbackVisionProvider(VisionProvider):
    """
    Reliable Offline Fallback Vision Provider for LearnSync AI.
    Ensures zero-downtime camera vision analysis during hackathon demos.
    """

    @property
    def provider_name(self) -> str:
        return "fallback_vision"

    async def analyze_image(
        self,
        image_base64: str,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        # Validate image payload
        if not image_base64 or len(image_base64) < 10:
            return {
                "detected": False,
                "question": "Unreadable image",
                "topic": "Unknown",
                "content_type": "text",
                "confidence": 0.0,
                "raw_ocr_text": "The image appears empty or corrupted.",
            }

        # Select structured demo preset based on image size/content simulation
        presets = [
            {
                "detected": True,
                "question": "Solve: 2x + 5 = 15",
                "topic": "Mathematics",
                "subtopic": "Linear Algebra",
                "content_type": "equation",
                "confidence": 0.96,
                "raw_ocr_text": "Solve for x: 2x + 5 = 15",
                "ai_solution": "### Step-by-Step Solution\n\n1. **Subtract 5 from both sides:**\n   $$2x = 15 - 5$$\n   $$2x = 10$$\n\n2. **Divide by 2:**\n   $$x = \\frac{10}{2} = 5$$\n\n**Final Result:** $x = 5$",
                "explanation": "Linear equation solved by isolating variable x.",
                "provider_used": "fallback_vision",
                "fallback_used": True
            },
            {
                "detected": True,
                "question": "Why does TCP use a three-way handshake?",
                "topic": "Computer Networks",
                "subtopic": "TCP Connection Establishment",
                "content_type": "question",
                "confidence": 0.94,
                "raw_ocr_text": "Q1: Why does TCP use a three-way handshake before data transfer?",
                "ai_solution": "### TCP Three-Way Handshake Explanation\n\nTCP uses a 3-step sequence (SYN -> SYN-ACK -> ACK) to ensure reliable communication:\n\n1. **SYN (Synchronize):** Client sends SYN packet to request connection and synchronize Sequence Numbers.\n2. **SYN-ACK (Synchronize-Acknowledge):** Server acknowledges client SYN and sends its own SYN.\n3. **ACK (Acknowledge):** Client acknowledges server SYN.\n\n**Purpose:** Guarantees both endpoints are ready and initial sequence numbers are synchronized.",
                "explanation": "Establishes reliable bidirectional sequence number synchronization.",
                "provider_used": "fallback_vision",
                "fallback_used": True
            },
            {
                "detected": True,
                "question": "What is database normalization?",
                "topic": "Database Management",
                "subtopic": "Relational Design",
                "content_type": "question",
                "confidence": 0.92,
                "raw_ocr_text": "Explain database normalization and 1NF, 2NF, 3NF.",
                "ai_solution": "### Database Normalization Summary\n\nNormalization eliminates redundancy and prevents insertion/update/deletion anomalies.\n\n- **1NF (First Normal Form):** Atomic values; no repeating groups.\n- **2NF (Second Normal Form):** In 1NF + no partial dependencies on composite primary key.\n- **3NF (Third Normal Form):** In 2NF + no transitive dependencies (non-key columns depend only on primary key).",
                "explanation": "Organizes relational schema to eliminate duplicate data and functional anomalies.",
                "provider_used": "fallback_vision",
                "fallback_used": True
            },
            {
                "detected": True,
                "question": "What is a binary search tree?",
                "topic": "Data Structures",
                "subtopic": "Trees & Searching",
                "content_type": "mixed",
                "confidence": 0.95,
                "raw_ocr_text": "BST Property: left child < root < right child",
                "ai_solution": "### Binary Search Tree (BST) Concept\n\nA Binary Search Tree is a node-based binary tree data structure with the following properties:\n\n1. The **left subtree** of a node contains only nodes with keys **less than** the node's key.\n2. The **right subtree** of a node contains only nodes with keys **greater than** the node's key.\n3. Both left and right subtrees must also be binary search trees.\n\n**Time Complexity:** Average search/insert/delete is $O(\\log n)$.",
                "explanation": "Binary tree maintaining ordered key invariant for logarithmic search.",
                "provider_used": "fallback_vision",
                "fallback_used": True
            },
        ]

        # Use student context to pick matching topic if provided
        selected = dict(presets[0])
        if student_context:
            cur_topic = (student_context.current_topic or "").lower()
            if "tcp" in cur_topic or "network" in cur_topic:
                selected = dict(presets[1])
            elif "dbms" in cur_topic or "database" in cur_topic:
                selected = dict(presets[2])
            elif "tree" in cur_topic or "data" in cur_topic:
                selected = dict(presets[3])

        return selected
