from typing import List, Optional, Dict, Any, Tuple
import uuid
from ..models.learning_models import RecommendationModel, TopicMasteryModel

class RecommendationService:
    """
    Generates prioritized, explainable learning recommendations and selects
    the Next Best Action for the student based on learning profile analysis.
    """

    @staticmethod
    def generate_recommendations(
        topic_masteries: List[TopicMasteryModel],
        repeated_mistakes: List[Dict[str, Any]]
    ) -> Tuple[List[RecommendationModel], Optional[RecommendationModel]]:
        recommendations: List[RecommendationModel] = []
        repeated_subtopics = {m["subtopic"].lower() for m in repeated_mistakes if "subtopic" in m}

        for tm in topic_masteries:
            topic_name = tm.subtopic if tm.subtopic else tm.topic
            sub_key = topic_name.lower()
            
            # Rule 1: High Priority — Repeated mistakes OR Mastery < 60% (Needs Practice)
            if sub_key in repeated_subtopics or tm.mastery_score < 60 or tm.trend == "declining":
                reason = f"You scored {tm.mastery_score}% and need additional practice on {topic_name}."
                if sub_key in repeated_subtopics:
                    reason = f"Repeated difficulty detected in {topic_name}. You answered multiple questions incorrectly."
                elif tm.trend == "declining":
                    reason = f"Performance in {topic_name} is declining. Revise key concepts before your next test."

                recommendations.append(RecommendationModel(
                    id=f"rec_{uuid.uuid4().hex[:6]}",
                    title=f"Revise {topic_name}",
                    subject=tm.subject,
                    topic=tm.topic,
                    subtopic=tm.subtopic,
                    reason=reason,
                    priority="high",
                    action="revision" if tm.mastery_score < 50 else "practice",
                    estimated_time_minutes=10,
                    difficulty="easy" if tm.mastery_score < 50 else "medium"
                ))

            # Rule 2: Medium Priority — Moderate mastery (60% - 79%)
            elif 60 <= tm.mastery_score < 80:
                recommendations.append(RecommendationModel(
                    id=f"rec_{uuid.uuid4().hex[:6]}",
                    title=f"Practice {topic_name}",
                    subject=tm.subject,
                    topic=tm.topic,
                    subtopic=tm.subtopic,
                    reason=f"Your mastery in {topic_name} is {tm.mastery_score}%. Practice to reach Strong mastery.",
                    priority="medium",
                    action="practice",
                    estimated_time_minutes=15,
                    difficulty="medium"
                ))

            # Rule 3: Low Priority — Strong mastery (80% - 89%) needing occasional reinforcement
            elif 80 <= tm.mastery_score < 90:
                recommendations.append(RecommendationModel(
                    id=f"rec_{uuid.uuid4().hex[:6]}",
                    title=f"Challenge Assessment: {topic_name}",
                    subject=tm.subject,
                    topic=tm.topic,
                    subtopic=tm.subtopic,
                    reason=f"Strong performance ({tm.mastery_score}%). Take a hard assessment to test your depth.",
                    priority="low",
                    action="assessment",
                    estimated_time_minutes=15,
                    difficulty="hard"
                ))

        # Sort recommendations by Priority (high > medium > low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda r: priority_order.get(r.priority, 3))

        # Next Best Action: First high priority recommendation, or default
        next_best_action = recommendations[0] if recommendations else None
        
        return recommendations, next_best_action
