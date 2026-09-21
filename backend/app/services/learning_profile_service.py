from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.learning_models import (
    LearningProfileModel,
    SubjectMasteryModel,
    TopicMasteryModel,
    RecommendationModel,
)
from .learning_gap_service import LearningGapService
from .recommendation_service import RecommendationService

class LearningProfileService:
    """
    Core state manager for Student Learning Profiles. Maintains assessment history,
    calculates subject & overall mastery, classifies strong/moderate/weak topics,
    and updates learning recommendations.
    """

    def __init__(self):
        self._history: List[Dict[str, Any]] = []
        self._mistakes: List[Dict[str, Any]] = []
        self._profile: LearningProfileModel = self._build_default_profile()

    def _build_default_profile(self) -> LearningProfileModel:
        """
        Builds initial default demo profile for hackathon demonstration.
        Default scenario:
        - Computer Networks: 82% (TCP Basics 95% Strong, TCP Handshake 75% Moderate, TCP Connection Termination 42% Needs Practice)
        - Data Structures: 76% (Arrays 92% Strong, Trees 60% Moderate)
        - DBMS: 71% (SQL 85% Moderate, Transactions 58% Needs Practice)
        - Operating Systems: 58% (Processes 70% Moderate, Scheduling 45% Needs Practice)
        """
        cn_topics = [
            TopicMasteryModel(subject="Computer Networks", topic="Computer Networks", subtopic="TCP Basics", mastery_score=95, attempts=10, correct=9, incorrect=1, trend="improving", status="strong"),
            TopicMasteryModel(subject="Computer Networks", topic="Computer Networks", subtopic="TCP Handshake", mastery_score=75, attempts=8, correct=6, incorrect=2, trend="stable", status="moderate"),
            TopicMasteryModel(subject="Computer Networks", topic="Computer Networks", subtopic="TCP Connection Termination", mastery_score=42, attempts=7, correct=3, incorrect=4, trend="declining", status="needs_practice")
        ]
        ds_topics = [
            TopicMasteryModel(subject="Data Structures", topic="Data Structures", subtopic="Arrays & Lists", mastery_score=92, attempts=12, correct=11, incorrect=1, trend="improving", status="strong"),
            TopicMasteryModel(subject="Data Structures", topic="Data Structures", subtopic="Binary Trees", mastery_score=60, attempts=5, correct=3, incorrect=2, trend="stable", status="moderate")
        ]
        db_topics = [
            TopicMasteryModel(subject="DBMS", topic="DBMS", subtopic="SQL & Normalization", mastery_score=85, attempts=10, correct=8, incorrect=2, trend="improving", status="moderate"),
            TopicMasteryModel(subject="DBMS", topic="DBMS", subtopic="Transactions & Locking", mastery_score=58, attempts=6, correct=3, incorrect=3, trend="declining", status="needs_practice")
        ]
        os_topics = [
            TopicMasteryModel(subject="Operating Systems", topic="Operating Systems", subtopic="Process Scheduling", mastery_score=45, attempts=8, correct=3, incorrect=5, trend="declining", status="needs_practice"),
            TopicMasteryModel(subject="Operating Systems", topic="Operating Systems", subtopic="Threads & Memory", mastery_score=70, attempts=7, correct=5, incorrect=2, trend="stable", status="moderate")
        ]

        subjects = {
            "Computer Networks": SubjectMasteryModel(subject="Computer Networks", overall_mastery=82, topics=cn_topics),
            "Data Structures": SubjectMasteryModel(subject="Data Structures", overall_mastery=76, topics=ds_topics),
            "DBMS": SubjectMasteryModel(subject="DBMS", overall_mastery=71, topics=db_topics),
            "Operating Systems": SubjectMasteryModel(subject="Operating Systems", overall_mastery=58, topics=os_topics),
        }

        all_topics = cn_topics + ds_topics + db_topics + os_topics
        strong = [t.subtopic for t in all_topics if t.status == "strong"]
        moderate = [t.subtopic for t in all_topics if t.status == "moderate"]
        weak = [t.subtopic for t in all_topics if t.status == "needs_practice"]

        recs, next_best = RecommendationService.generate_recommendations(all_topics, [
            {"subtopic": "TCP Connection Termination", "topic": "Computer Networks"},
            {"subtopic": "TCP Connection Termination", "topic": "Computer Networks"}
        ])

        return LearningProfileModel(
            student_id="student_001",
            overall_mastery=78,
            strong_topics=strong,
            moderate_topics=moderate,
            weak_topics=weak,
            subjects=subjects,
            trends=[{"subject": "Computer Networks", "trend": "improving"}, {"subject": "Operating Systems", "trend": "declining"}],
            recommendations=recs,
            next_best_action=next_best
        )

    def get_profile(self) -> LearningProfileModel:
        return self._profile

    def update_from_assessment_result(
        self,
        subject: str,
        topic: str,
        percentage: int,
        submissions: List[Dict[str, Any]],
        mistakes: List[Dict[str, Any]]
    ) -> LearningProfileModel:
        """
        Updates topic mastery, strong/weak areas, repeated mistakes,
        and recommendations after a completed assessment or practice session.
        """
        self._history.append({
            "subject": subject,
            "topic": topic,
            "percentage": percentage,
            "timestamp": datetime.now().isoformat()
        })
        self._mistakes.extend(mistakes)

        # 1. Update or create subject mastery
        if subject not in self._profile.subjects:
            self._profile.subjects[subject] = SubjectMasteryModel(subject=subject, overall_mastery=percentage, topics=[])

        subject_mastery = self._profile.subjects[subject]
        
        # Group submissions by subtopic
        subtopic_stats: Dict[str, Dict[str, int]] = {}
        for sub in submissions:
            st_name = sub.get("subtopic") or topic
            if st_name not in subtopic_stats:
                subtopic_stats[st_name] = {"correct": 0, "total": 0}
            subtopic_stats[st_name]["total"] += 1
            if sub.get("selected_key") == sub.get("correct_key"):
                subtopic_stats[st_name]["correct"] += 1

        # 2. Update each topic mastery in subject
        existing_topics_map = {t.subtopic: t for t in subject_mastery.topics if t.subtopic}
        for st_name, stats in subtopic_stats.items():
            recent_sub_score = round((stats["correct"] / stats["total"]) * 100) if stats["total"] > 0 else percentage
            
            if st_name in existing_topics_map:
                tm = existing_topics_map[st_name]
                tm.attempts += stats["total"]
                tm.correct += stats["correct"]
                tm.incorrect += (stats["total"] - stats["correct"])
                tm.mastery_score = LearningGapService.calculate_topic_mastery(
                    recent_score=recent_sub_score,
                    total_correct=tm.correct,
                    total_attempts=tm.attempts
                )
                tm.status = LearningGapService.classify_status(tm.mastery_score)
                tm.last_practiced_at = datetime.now().isoformat()
            else:
                new_mastery = LearningGapService.calculate_topic_mastery(
                    recent_score=recent_sub_score,
                    total_correct=stats["correct"],
                    total_attempts=stats["total"]
                )
                new_tm = TopicMasteryModel(
                    subject=subject,
                    topic=topic,
                    subtopic=st_name,
                    mastery_score=new_mastery,
                    attempts=stats["total"],
                    correct=stats["correct"],
                    incorrect=stats["total"] - stats["correct"],
                    status=LearningGapService.classify_status(new_mastery),
                    last_practiced_at=datetime.now().isoformat()
                )
                subject_mastery.topics.append(new_tm)

        # 3. Recalculate subject overall mastery
        if subject_mastery.topics:
            subject_mastery.overall_mastery = round(
                sum(t.mastery_score for t in subject_mastery.topics) / len(subject_mastery.topics)
            )

        # 4. Recalculate overall profile mastery across all subjects
        all_subjects = list(self._profile.subjects.values())
        if all_subjects:
            self._profile.overall_mastery = round(
                sum(s.overall_mastery for s in all_subjects) / len(all_subjects)
            )

        # 5. Reclassify strong, moderate, weak topics across all subjects
        all_topics: List[TopicMasteryModel] = []
        for s in all_subjects:
            all_topics.extend(s.topics)

        self._profile.strong_topics = [t.subtopic for t in all_topics if t.status == "strong" and t.subtopic]
        self._profile.moderate_topics = [t.subtopic for t in all_topics if t.status == "moderate" and t.subtopic]
        self._profile.weak_topics = [t.subtopic for t in all_topics if t.status == "needs_practice" and t.subtopic]

        # 6. Detect repeated mistakes & update recommendations
        repeated = LearningGapService.detect_repeated_mistakes(self._mistakes)
        recs, next_best = RecommendationService.generate_recommendations(all_topics, repeated)

        self._profile.recommendations = recs
        self._profile.next_best_action = next_best

        return self._profile

    def reset_profile(self) -> LearningProfileModel:
        """Resets student learning profile back to default hackathon baseline."""
        self._history = []
        self._mistakes = []
        self._profile = self._build_default_profile()
        return self._profile

