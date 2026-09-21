from typing import List, Dict, Any, Tuple
from ..models.learning_models import TopicMasteryModel

class LearningGapService:
    """
    Detects learning gaps, calculates topic mastery, classifies performance statuses,
    tracks repeated subtopic mistakes, and calculates performance trends.
    """

    @staticmethod
    def calculate_topic_mastery(recent_score: int, total_correct: int, total_attempts: int) -> int:
        """
        Explainable formula:
        Mastery = min(100, round(0.6 * recent_score + 0.4 * historical_accuracy))
        """
        if total_attempts <= 0:
            return recent_score
        
        historical_accuracy = (total_correct / total_attempts) * 100.0
        weighted_mastery = (0.6 * recent_score) + (0.4 * historical_accuracy)
        return min(100, max(0, round(weighted_mastery)))

    @staticmethod
    def classify_status(mastery_score: int) -> str:
        """
        Strong: >= 90%
        Moderate: 60% - 89%
        Needs Practice: < 60%
        """
        if mastery_score >= 90:
            return "strong"
        elif mastery_score >= 60:
            return "moderate"
        else:
            return "needs_practice"

    @staticmethod
    def calculate_trend(scores: List[int]) -> str:
        """
        Calculates performance trend from a list of chronological scores.
        - Improving: Net positive trend e.g. 50 -> 60 -> 72
        - Declining: Net negative trend e.g. 85 -> 70 -> 55
        - Stable: Minimal variation e.g. 80 -> 78 -> 79
        """
        if len(scores) < 2:
            return "stable"
        
        diffs = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
        avg_diff = sum(diffs) / len(diffs)
        
        if avg_diff > 3.0:
            return "improving"
        elif avg_diff < -3.0:
            return "declining"
        else:
            return "stable"

    @staticmethod
    def detect_repeated_mistakes(mistakes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies subtopics where student has failed 2 or more questions.
        Returns a list of repeated mistake insights.
        """
        subtopic_counts: Dict[str, Dict[str, Any]] = {}
        
        for mistake in mistakes:
            subtopic = mistake.get("subtopic") or mistake.get("topic") or "General"
            if subtopic not in subtopic_counts:
                subtopic_counts[subtopic] = {
                    "subtopic": subtopic,
                    "topic": mistake.get("topic", "General"),
                    "count": 0,
                    "question_ids": []
                }
            subtopic_counts[subtopic]["count"] += 1
            if mistake.get("question_id"):
                subtopic_counts[subtopic]["question_ids"].append(mistake.get("question_id"))

        repeated = [
            item for item in subtopic_counts.values()
            if item["count"] >= 2
        ]
        return repeated
