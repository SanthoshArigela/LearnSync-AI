import random
from typing import Dict, Any, List, Optional
from .assessment_provider import AssessmentProvider
from ..models.tutor_models import StudentContextModel, QuizOptionModel

class FallbackAssessmentProvider(AssessmentProvider):
    """
    Reliable Offline Fallback Assessment Provider for LearnSync AI.
    Generates structured CS question sets for zero-downtime demos.
    """

    @property
    def provider_name(self) -> str:
        return "fallback_assessment"

    async def generate_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        student_context: Optional[StudentContextModel] = None
    ) -> Dict[str, Any]:
        pool = self._get_question_pool(subject, topic)
        selected_questions = pool[:question_count] if len(pool) >= question_count else pool

        return {
            "assessment_id": f"ass_{random.randint(1000, 9999)}",
            "subject": subject,
            "topic": topic,
            "requested_difficulty": difficulty,
            "questions": selected_questions,
            "provider_used": self.provider_name,
        }

    def _get_question_pool(self, subject: str, topic: str) -> List[Dict[str, Any]]:
        sub_lower = subject.lower()

        if "network" in sub_lower or "tcp" in topic.lower():
            return [
                {
                    "id": "cn_q1",
                    "question": "Which protocol provides reliable, connection-oriented communication?",
                    "topic": "TCP",
                    "subtopic": "TCP basics",
                    "difficulty": "medium",
                    "options": [
                        {"key": "A", "text": "UDP"},
                        {"key": "B", "text": "TCP"},
                        {"key": "C", "text": "IP"},
                        {"key": "D", "text": "ARP"},
                    ],
                    "correct_key": "B",
                    "explanation": "TCP establishes a 3-way handshake and tracks sequence numbers to guarantee reliable communication."
                },
                {
                    "id": "cn_q2",
                    "question": "Which layer of the OSI model handles logical IP addressing?",
                    "topic": "OSI Model",
                    "subtopic": "Layer 3",
                    "difficulty": "easy",
                    "options": [
                        {"key": "A", "text": "Data Link Layer"},
                        {"key": "B", "text": "Network Layer"},
                        {"key": "C", "text": "Transport Layer"},
                        {"key": "D", "text": "Application Layer"},
                    ],
                    "correct_key": "B",
                    "explanation": "The Network Layer (Layer 3) is responsible for IP routing and logical packet addressing."
                },
                {
                    "id": "cn_q3",
                    "question": "What is the primary function of Domain Name System (DNS)?",
                    "topic": "DNS",
                    "subtopic": "DNS resolution",
                    "difficulty": "easy",
                    "options": [
                        {"key": "A", "text": "Encrypting network packets"},
                        {"key": "B", "text": "Resolving domain names to IP addresses"},
                        {"key": "C", "text": "Managing hardware MAC addresses"},
                        {"key": "D", "text": "Detecting transmission collisions"},
                    ],
                    "correct_key": "B",
                    "explanation": "DNS translates human-readable domain names (e.g. google.com) to machine IP addresses."
                },
                {
                    "id": "cn_q4",
                    "question": "Which mechanism is used by TCP for flow control?",
                    "topic": "TCP",
                    "subtopic": "Flow Control",
                    "difficulty": "hard",
                    "options": [
                        {"key": "A", "text": "Sliding Window Protocol"},
                        {"key": "B", "text": "Stop and Wait"},
                        {"key": "C", "text": "Token Bucket"},
                        {"key": "D", "text": "CSMA/CD"},
                    ],
                    "correct_key": "A",
                    "explanation": "TCP uses dynamic sliding window mechanisms to regulate sender transmission rate based on receiver window buffer size."
                },
                {
                    "id": "cn_q5",
                    "question": "Which packet control sequence is used during TCP connection termination?",
                    "topic": "TCP",
                    "subtopic": "TCP connection termination",
                    "difficulty": "hard",
                    "options": [
                        {"key": "A", "text": "SYN - SYN-ACK - ACK"},
                        {"key": "B", "text": "FIN - ACK - FIN - ACK"},
                        {"key": "C", "text": "RST - ACK"},
                        {"key": "D", "text": "PING - PONG"},
                    ],
                    "correct_key": "B",
                    "explanation": "TCP connection release requires a four-way handshake using FIN and ACK control segments."
                },
            ]
        elif "data" in sub_lower or "tree" in topic.lower():
            return [
                {
                    "id": "ds_q1",
                    "question": "Which data structure operates on a First In First Out (FIFO) basis?",
                    "topic": "Queues",
                    "subtopic": "FIFO ordering",
                    "difficulty": "easy",
                    "options": [
                        {"key": "A", "text": "Stack"},
                        {"key": "B", "text": "Queue"},
                        {"key": "C", "text": "Tree"},
                        {"key": "D", "text": "Graph"},
                    ],
                    "correct_key": "B",
                    "explanation": "Queue is a FIFO structure where the element added first is removed first."
                },
                {
                    "id": "ds_q2",
                    "question": "What is the worst-case time complexity of searching in an unbalanced Binary Search Tree?",
                    "topic": "Trees",
                    "subtopic": "BST search complexity",
                    "difficulty": "hard",
                    "options": [
                        {"key": "A", "text": "O(1)"},
                        {"key": "B", "text": "O(log n)"},
                        {"key": "C", "text": "O(n)"},
                        {"key": "D", "text": "O(n log n)"},
                    ],
                    "correct_key": "C",
                    "explanation": "An unbalanced BST can degenerate into a linked list, yielding O(n) search time."
                }
            ]
        elif "dbms" in sub_lower or "database" in sub_lower:
            return [
                {
                    "id": "db_q1",
                    "question": "What does ACID stand for in DBMS transactions?",
                    "topic": "Transactions",
                    "subtopic": "ACID properties",
                    "difficulty": "medium",
                    "options": [
                        {"key": "A", "text": "Atomicity, Consistency, Isolation, Durability"},
                        {"key": "B", "text": "Array, Column, Index, Database"},
                        {"key": "C", "text": "Access, Control, Interface, Data"},
                        {"key": "D", "text": "Aggregation, Concurrency, Integrity, Deletion"},
                    ],
                    "correct_key": "A",
                    "explanation": "ACID properties guarantee reliable transaction execution in relational databases."
                }
            ]
        else: # OS
            return [
                {
                    "id": "os_q1",
                    "question": "Which scheduling algorithm can cause starvation for long processes?",
                    "topic": "Operating Systems",
                    "subtopic": "Process scheduling",
                    "difficulty": "hard",
                    "options": [
                        {"key": "A", "text": "First-Come First-Served (FCFS)"},
                        {"key": "B", "text": "Shortest Job First (SJF)"},
                        {"key": "C", "text": "Round Robin (RR)"},
                        {"key": "D", "text": "FIFO"},
                    ],
                    "correct_key": "B",
                    "explanation": "SJF favors short jobs, causing starvation for longer processes if short jobs arrive continuously."
                }
            ]
