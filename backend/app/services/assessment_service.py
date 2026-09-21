from typing import Dict, List, Any, Optional
from ..models.assessment_models import (
    AssessmentGenerateRequest,
    AssessmentGenerateResponse,
    GeneratedQuestionModel,
    AssessmentEvaluateRequest,
    AssessmentEvaluateResponse,
)
from ..providers.assessment_provider import AssessmentProvider
from ..providers.gemini_assessment_provider import GeminiAssessmentProvider

class AssessmentService:
    def __init__(self, provider: Optional[AssessmentProvider] = None):
        self.provider = provider or GeminiAssessmentProvider()

    async def generate_assessment(self, req: AssessmentGenerateRequest) -> AssessmentGenerateResponse:
        raw_res = await self.provider.generate_questions(
            subject=req.subject,
            topic=req.topic,
            difficulty=req.difficulty,
            question_count=req.question_count,
            student_context=req.student_context
        )

        questions_raw = raw_res.get("questions", [])
        questions = [GeneratedQuestionModel(**q) for q in questions_raw]

        return AssessmentGenerateResponse(
            assessment_id=raw_res.get("assessment_id", "ass_101"),
            subject=raw_res.get("subject", req.subject),
            topic=raw_res.get("topic", req.topic),
            requested_difficulty=raw_res.get("requested_difficulty", req.difficulty),
            questions=questions,
            provider_used=raw_res.get("provider_used", self.provider.provider_name)
        )

    def evaluate_assessment(self, req: AssessmentEvaluateRequest) -> AssessmentEvaluateResponse:
        total = len(req.submissions)
        if total == 0:
            return AssessmentEvaluateResponse(
                assessment_id=req.assessment_id,
                score=0,
                total=0,
                percentage=0,
                strong_areas=[],
                needs_practice=[],
                ai_recommendation="Complete an assessment to get recommendations.",
            )

        correct_count = 0
        topic_scores: Dict[str, Dict[str, int]] = {}
        mistakes = []

        for sub in req.submissions:
            subtopic = sub.subtopic or sub.topic
            if subtopic not in topic_scores:
                topic_scores[subtopic] = {"correct": 0, "total": 0}

            topic_scores[subtopic]["total"] += 1

            is_correct = sub.selected_key.strip().upper() == sub.correct_key.strip().upper()
            if is_correct:
                correct_count += 1
                topic_scores[subtopic]["correct"] += 1
            else:
                mistakes.append({
                    "question_id": sub.question_id,
                    "question": sub.question_text,
                    "selected_key": sub.selected_key,
                    "correct_key": sub.correct_key,
                    "explanation": sub.explanation,
                    "subtopic": subtopic,
                })

        score_pct = int((correct_count / total) * 100)

        strong_areas = [t for t, data in topic_scores.items() if data["correct"] == data["total"]]
        needs_practice = [t for t, data in topic_scores.items() if data["correct"] < data["total"]]

        if not needs_practice and score_pct == 100:
            recommendation = f"Outstanding performance! You mastered all topics in {req.subject}."
        elif needs_practice:
            weak_str = ", ".join(needs_practice[:2])
            recommendation = f"You may need more practice with {weak_str}. Spend 10 minutes reviewing these topics before your next assessment."
        else:
            recommendation = f"Good effort! Review key concepts in {req.subject} to improve further."

        adaptive_summary = None
        if req.adaptive_path:
            path_str = " → ".join(req.adaptive_path)
            adaptive_summary = f"Adaptive Difficulty Path: {path_str}"

        # Trigger Sprint 5 Learning Profile Update
        try:
            from ..api.learning import learning_profile_service
            submissions_dict = [sub.model_dump() for sub in req.submissions]
            learning_profile_service.update_from_assessment_result(
                subject=req.subject,
                topic=req.topic,
                percentage=score_pct,
                submissions=submissions_dict,
                mistakes=mistakes
            )
        except Exception:
            pass  # Gracefully proceed if profile update encounters an issue

        return AssessmentEvaluateResponse(
            assessment_id=req.assessment_id,
            score=correct_count,
            total=total,
            percentage=score_pct,
            strong_areas=strong_areas if strong_areas else [f"{req.topic} basics"],
            needs_practice=needs_practice if needs_practice else [f"{req.topic} advanced concepts"],
            ai_recommendation=recommendation,
            adaptive_path_summary=adaptive_summary,
            mistakes=mistakes,
        )

