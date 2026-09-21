from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from ..models.teacher_models import (
    TeacherDashboardModel,
    StudentClassSummaryModel,
    StudentDetailModel,
    ClassTopicInsightModel,
    TeacherRecommendationModel,
    TeachingActivityCreateRequest,
    TeachingActivityModel,
    AssessmentAnalyticsModel,
)
from ..services.teacher_service import TeacherService

router = APIRouter(prefix="/api/teacher", tags=["teacher"])
teacher_service = TeacherService()

@router.get("/dashboard", response_model=TeacherDashboardModel)
async def get_teacher_dashboard():
    """
    Returns high-level classroom performance metrics, weak topics,
    misconceptions, students needing attention, and AI recommendations.
    """
    try:
        return teacher_service.get_dashboard()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch teacher dashboard data", "details": str(e)}
        )

@router.get("/students", response_model=List[StudentClassSummaryModel])
async def get_students():
    """
    Returns class student summaries, mastery scores, weak topics, and trends.
    """
    try:
        return teacher_service.get_students()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch students list", "details": str(e)}
        )

@router.get("/students/{student_id}", response_model=StudentDetailModel)
async def get_student_detail(student_id: str):
    """
    Returns deep-dive learning profile, subject masteries, and recent activities for a student.
    """
    try:
        return teacher_service.get_student_detail(student_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to fetch student details for {student_id}", "details": str(e)}
        )

@router.get("/topics", response_model=List[ClassTopicInsightModel])
async def get_topics():
    """
    Returns classroom-level topic masteries, affected student counts, and severity tags.
    """
    try:
        return teacher_service.get_topics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch classroom topic insights", "details": str(e)}
        )

@router.get("/topics/{topic_id}")
async def get_topic_detail(topic_id: str):
    """
    Returns topic intelligence including mastery distribution, struggling students, and common mistakes.
    """
    try:
        return teacher_service.get_topic_detail(topic_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"Failed to fetch topic details for {topic_id}", "details": str(e)}
        )

@router.get("/assessments", response_model=List[AssessmentAnalyticsModel])
async def get_assessments():
    """
    Returns assessment analytics, completion rates, average scores, and difficult concepts.
    """
    try:
        return teacher_service.get_assessments()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch assessment analytics", "details": str(e)}
        )

@router.get("/recommendations", response_model=List[TeacherRecommendationModel])
async def get_recommendations():
    """
    Returns explainable AI teacher recommendations (WHAT, WHO, WHY, ACTION).
    """
    try:
        return teacher_service.get_recommendations()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to fetch teacher recommendations", "details": str(e)}
        )

@router.post("/activities", response_model=TeachingActivityModel)
async def create_targeted_activity(req: TeachingActivityCreateRequest):
    """
    Creates a lightweight targeted revision/practice activity for struggling students.
    """
    try:
        return teacher_service.create_activity(req)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to create teaching activity", "details": str(e)}
        )

@router.post("/demo/reset")
async def reset_demo_state():
    """
    Resets teacher dashboard analytics and classroom collaboration events to baseline hackathon demo state.
    """
    try:
        return teacher_service.reset_demo()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to reset demo state", "details": str(e)}
        )

@router.get("/health")
async def teacher_health_check():
    return {
        "status": "healthy",
        "service": "LearnSync AI Teacher Intelligence"
    }
