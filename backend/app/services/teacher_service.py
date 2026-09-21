from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from ..models.teacher_models import (
    TeacherDashboardModel,
    StudentClassSummaryModel,
    StudentDetailModel,
    ClassTopicInsightModel,
    ClassMisconceptionModel,
    TeacherRecommendationModel,
    TeachingActivityCreateRequest,
    TeachingActivityModel,
    AssessmentAnalyticsModel,
)
from .learning_profile_service import LearningProfileService

class TeacherService:
    """
    Classroom Intelligence Aggregator for LearnSync AI Teacher Intelligence Dashboard.
    Combines student learning profiles, topic masteries, assessment results, and AI recommendations.
    """

    def __init__(self):
        self._activities: List[TeachingActivityModel] = []
        self._students = self._build_demo_students()
        self._topics = self._build_demo_topics()
        self._misconceptions = self._build_demo_misconceptions()
        self._recommendations = self._build_demo_recommendations()
        self._assessments = self._build_demo_assessments()

    def _build_demo_students(self) -> List[StudentClassSummaryModel]:
        return [
            StudentClassSummaryModel(
                student_id="student_001",
                name="Santhosh K.",
                overall_mastery=52,
                weak_topic="Process Scheduling",
                trend="declining",
                recommended_action="Assign Round Robin practice questions"
            ),
            StudentClassSummaryModel(
                student_id="student_002",
                name="Ananya Sharma",
                overall_mastery=58,
                weak_topic="DBMS Normalization",
                trend="stable",
                recommended_action="Review 3NF decomposition examples"
            ),
            StudentClassSummaryModel(
                student_id="student_003",
                name="Rahul Verma",
                overall_mastery=61,
                weak_topic="TCP Connection Termination",
                trend="declining",
                recommended_action="Review 4-way FIN handshake sequence"
            ),
            StudentClassSummaryModel(
                student_id="student_004",
                name="Priya Patel",
                overall_mastery=64,
                weak_topic="Binary Search Trees",
                trend="improving",
                recommended_action="Practice tree traversal questions"
            ),
            StudentClassSummaryModel(
                student_id="student_005",
                name="Vikram Singh",
                overall_mastery=55,
                weak_topic="Process Scheduling",
                trend="declining",
                recommended_action="Review Priority Preemption rules"
            ),
            StudentClassSummaryModel(
                student_id="student_006",
                name="Sneha Reddy",
                overall_mastery=59,
                weak_topic="TCP Connection Termination",
                trend="declining",
                recommended_action="Review FIN-WAIT-1 and TIME-WAIT states"
            ),
            StudentClassSummaryModel(
                student_id="student_007",
                name="Arjun Nair",
                overall_mastery=57,
                weak_topic="DBMS Transactions",
                trend="stable",
                recommended_action="Review ACID Isolation levels"
            ),
            StudentClassSummaryModel(
                student_id="student_008",
                name="Kavya Gupta",
                overall_mastery=54,
                weak_topic="Process Scheduling",
                trend="declining",
                recommended_action="Review SJF Gantt Chart calculations"
            ),
        ]

    def _build_demo_topics(self) -> List[ClassTopicInsightModel]:
        return [
            ClassTopicInsightModel(
                id="topic_os_sched",
                topic="Process Scheduling",
                subject="Operating Systems",
                class_mastery=58,
                affected_students_count=17,
                severity="HIGH",
                recommended_teaching_action="Conduct a 10-minute revision on Round Robin & Priority Scheduling.",
                trend="declining"
            ),
            ClassTopicInsightModel(
                id="topic_tcp_term",
                topic="TCP Connection Termination",
                subject="Computer Networks",
                class_mastery=54,
                affected_students_count=14,
                severity="HIGH",
                recommended_teaching_action="Use a TCP 4-way FIN handshake sequence diagram.",
                trend="declining"
            ),
            ClassTopicInsightModel(
                id="topic_db_norm",
                topic="Database Normalization",
                subject="DBMS",
                class_mastery=61,
                affected_students_count=11,
                severity="MEDIUM",
                recommended_teaching_action="Solve 2 functional dependency BCNF decomposition examples.",
                trend="stable"
            ),
            ClassTopicInsightModel(
                id="topic_tree_trav",
                topic="Binary Trees & Traversal",
                subject="Data Structures",
                class_mastery=76,
                affected_students_count=5,
                severity="LOW",
                recommended_teaching_action="Provide an optional advanced tree balancing exercise.",
                trend="improving"
            ),
            ClassTopicInsightModel(
                id="topic_tcp_handshake",
                topic="TCP 3-Way Handshake",
                subject="Computer Networks",
                class_mastery=82,
                affected_students_count=3,
                severity="LOW",
                recommended_teaching_action="Briefly review SYN-ACK sequence numbers before midterms.",
                trend="improving"
            ),
        ]

    def _build_demo_misconceptions(self) -> List[ClassMisconceptionModel]:
        return [
            ClassMisconceptionModel(
                id="misc_os_1",
                topic="Process Scheduling",
                subject="Operating Systems",
                misconception_text="Students are confusing waiting time with turnaround time in non-preemptive SJF.",
                affected_students_count=14,
                recommended_resource="Use a step-by-step Gantt chart timeline comparison before next quiz."
            ),
            ClassMisconceptionModel(
                id="misc_tcp_1",
                topic="TCP Connection Termination",
                subject="Computer Networks",
                misconception_text="Students are confusing SYN-ACK with final connection establishment and missing FIN ACK steps.",
                affected_students_count=12,
                recommended_resource="Display an interactive TCP 4-way FIN state diagram during lecture."
            ),
            ClassMisconceptionModel(
                id="misc_db_1",
                topic="Database Normalization",
                subject="DBMS",
                misconception_text="Students confuse 3NF transitive dependency rules with 2NF partial dependency rules.",
                affected_students_count=9,
                recommended_resource="Review candidate key determination techniques in class."
            )
        ]

    def _build_demo_recommendations(self) -> List[TeacherRecommendationModel]:
        return [
            TeacherRecommendationModel(
                id="rec_t_1",
                priority="HIGH",
                topic="Process Scheduling",
                subject="Operating Systems",
                affected_students_count=17,
                why_evidence="17 students scored below 60% mastery and 14 made repeated Gantt chart calculation mistakes.",
                recommended_action="Conduct a 10-minute revision covering Round Robin time-quantum preemption rules.",
                expected_goal="Improve class scheduling concept mastery from 58% to 75% before next quiz."
            ),
            TeacherRecommendationModel(
                id="rec_t_2",
                priority="HIGH",
                topic="TCP Connection Termination",
                subject="Computer Networks",
                affected_students_count=14,
                why_evidence="14 students failed questions on TIME-WAIT and FIN-WAIT-2 state transitions.",
                recommended_action="Display a TCP 4-way FIN sequence diagram and send 5 targeted practice questions.",
                expected_goal="Eliminate connection release misconceptions across Section A."
            ),
            TeacherRecommendationModel(
                id="rec_t_3",
                priority="MEDIUM",
                topic="Database Normalization",
                subject="DBMS",
                affected_students_count=11,
                why_evidence="11 students scored between 60% and 65% on BCNF decomposition tests.",
                recommended_action="Assign a 5-question adaptive revision set focusing on candidate key extraction.",
                expected_goal="Push moderate students to Strong mastery (>= 80%)."
            )
        ]

    def _build_demo_assessments(self) -> List[AssessmentAnalyticsModel]:
        return [
            AssessmentAnalyticsModel(
                id="assess_1",
                title="Operating Systems Midterm Quiz 1",
                subject="Operating Systems",
                topic="Process Scheduling",
                total_students=42,
                average_score=58,
                completion_rate=95,
                most_difficult_question="Calculate turnaround time for SJF with arrival times [0, 2, 4].",
                most_difficult_concept="Gantt chart timeline calculation"
            ),
            AssessmentAnalyticsModel(
                id="assess_2",
                title="Computer Networks Quiz 2",
                subject="Computer Networks",
                topic="TCP Connection Termination",
                total_students=42,
                average_score=68,
                completion_rate=98,
                most_difficult_question="Which socket state follows FIN-WAIT-1 upon receiving ACK?",
                most_difficult_concept="4-Way FIN state machine"
            ),
            AssessmentAnalyticsModel(
                id="assess_3",
                title="DBMS Quiz 1",
                subject="DBMS",
                topic="Database Normalization",
                total_students=42,
                average_score=71,
                completion_rate=92,
                most_difficult_question="Identify non-prime attribute transitive dependencies in R(A,B,C,D).",
                most_difficult_concept="3NF decomposition"
            )
        ]

    def get_dashboard(self) -> TeacherDashboardModel:
        return TeacherDashboardModel(
            class_name="B.Tech CSE — AI & ML",
            section="Section A",
            total_students=42,
            average_score=78,
            students_needing_attention_count=len(self._students),
            improving_students_count=24,
            subject_performances={
                "Computer Networks": 82,
                "Data Structures": 76,
                "DBMS": 71,
                "Operating Systems": 58,
                "Machine Learning": 64,
            },
            classroom_gaps=self._topics[:3],
            misconceptions=self._misconceptions,
            students_needing_attention=self._students,
            recommendations=self._recommendations,
            recent_activities=self._activities
        )

    def get_students(self) -> List[StudentClassSummaryModel]:
        return self._students

    def get_student_detail(self, student_id: str) -> StudentDetailModel:
        student = next((s for s in self._students if s.student_id == student_id), None)
        name = student.name if student else "Santhosh K."
        mastery = student.overall_mastery if student else 52
        weak = student.weak_topic if student else "Process Scheduling"

        return StudentDetailModel(
            student_id=student_id,
            name=name,
            course="B.Tech CSE — AI & ML (Section A)",
            overall_mastery=mastery,
            recent_assessment_score=48,
            trend=student.trend if student else "declining",
            subject_masteries={
                "Computer Networks": 82,
                "Data Structures": 76,
                "DBMS": 65,
                "Operating Systems": 48,
                "Machine Learning": 70,
            },
            weak_topics=[weak, "Threads & Memory"],
            recent_activities=[
                {"type": "assessment", "title": "Operating Systems Quiz 1", "score": "45%", "date": "2 hours ago"},
                {"type": "tutor", "title": "Asked AI Tutor about FIN handshake", "date": "Yesterday"},
                {"type": "practice", "title": "Completed 5 adaptive practice questions", "score": "60%", "date": "2 days ago"},
            ],
            recommended_action=f"Assign a 10-minute targeted revision set on {weak}."
        )

    def get_topics(self) -> List[ClassTopicInsightModel]:
        return self._topics

    def get_topic_detail(self, topic_id: str) -> Dict[str, Any]:
        topic = next((t for t in self._topics if t.id == topic_id), self._topics[0])
        return {
            "id": topic.id,
            "topic": topic.topic,
            "subject": topic.subject,
            "class_mastery": topic.class_mastery,
            "affected_students_count": topic.affected_students_count,
            "severity": topic.severity,
            "trend": topic.trend,
            "mastery_distribution": {
                "strong": 12,
                "moderate": 13,
                "needs_practice": topic.affected_students_count
            },
            "struggling_students": [s.name for s in self._students if topic.topic in s.weak_topic or "Scheduling" in topic.topic],
            "common_mistakes": [m.misconception_text for m in self._misconceptions if m.topic == topic.topic],
            "recommended_teaching_action": topic.recommended_teaching_action
        }

    def get_assessments(self) -> List[AssessmentAnalyticsModel]:
        return self._assessments

    def get_recommendations(self) -> List[TeacherRecommendationModel]:
        return self._recommendations

    def create_activity(self, req: TeachingActivityCreateRequest) -> TeachingActivityModel:
        activity = TeachingActivityModel(
            id=f"act_{uuid.uuid4().hex[:6]}",
            topic=req.topic,
            subject=req.subject,
            activity_type=req.activity_type,
            target_student_ids=req.target_student_ids if req.target_student_ids else [s.student_id for s in self._students],
            question_count=req.question_count,
            difficulty=req.difficulty,
            status="created",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self._activities.insert(0, activity)

        # Sync with Classroom Collaboration Service
        try:
            from .collaboration_service import CollaborationService
            from ..models.collaboration_models import TeacherActionRequest
            collab = CollaborationService()
            action_req = TeacherActionRequest(
                action_type="START_REVISION",
                topic=req.topic,
                subject=req.subject,
                target_student_ids=activity.target_student_ids,
                question_count=req.question_count,
                difficulty=req.difficulty,
                message=f"Your teacher assigned a targeted revision on {req.topic} ({req.question_count} questions)."
            )
            # Dispatch sync action (in-memory pending queue & sockets)
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(collab.dispatch_teacher_action(action_req))
            except RuntimeError:
                # No running loop, update pending actions synchronously
                for st_id in activity.target_student_ids:
                    if st_id not in collab._pending_actions:
                        collab._pending_actions[st_id] = []
                    from ..models.collaboration_models import TeacherActionModel
                    collab._pending_actions[st_id].insert(0, TeacherActionModel(
                        action_id=activity.id,
                        action_type="START_REVISION",
                        topic=req.topic,
                        subject=req.subject,
                        target_student_ids=activity.target_student_ids,
                        question_count=req.question_count,
                        difficulty=req.difficulty,
                        message=f"Your teacher assigned a targeted revision on {req.topic}.",
                        status="delivered",
                        created_at=activity.created_at
                    ))
        except Exception as e:
            print(f"Collaboration sync warning: {e}")

        return activity

    def reset_demo(self) -> Dict[str, Any]:
        """Resets teacher dashboard, student learning profile, and classroom collaboration demo state."""
        self._activities = []
        self._students = self._build_demo_students()
        self._topics = self._build_demo_topics()
        self._misconceptions = self._build_demo_misconceptions()
        self._recommendations = self._build_demo_recommendations()
        self._assessments = self._build_demo_assessments()

        # Reset Learning Profile state
        try:
            profile_service = LearningProfileService()
            profile_service.reset_profile()
        except Exception as e:
            print(f"Profile reset warning: {e}")

        # Reset Collaboration events buffer & pending actions
        from .collaboration_service import CollaborationService
        collab = CollaborationService()
        collab._events_buffer = collab._build_demo_initial_events()
        collab._pending_actions = {}

        return {"status": "success", "message": "Demo state successfully reset to baseline."}

