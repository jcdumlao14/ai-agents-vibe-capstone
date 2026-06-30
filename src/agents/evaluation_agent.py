from typing import Any, Dict, List

from src.config.logger import logger


class EvaluationAgent:
    """Evaluation agent to assess recommendation quality and business alignment."""

    def __init__(self):
        self.name = "BusinessPilot Evaluation Agent"
        self.version = "0.1.0"

    def evaluate(
        self,
        customer: Dict[str, Any],
        recommendations: Dict[str, Any],
        churn_score: float,
        explanation: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info("EvaluationAgent assessing recommendations for customer_id=%s", customer.get("customer_id"))

        actions = recommendations.get("actions", [])
        confidence = recommendations.get("confidence", 0.0)
        evaluation_score = self._compute_evaluation_score(churn_score, confidence, actions)
        issues = self._detect_issues(churn_score, explanation, recommendations, evaluation_score)
        improvement_suggestions = self._suggest_improvements(issues)

        result = {
            "status": "completed",
            "evaluation_score": evaluation_score,
            "action_count": len(actions),
            "confidence": confidence,
            "alignment": self._assess_alignment(churn_score, actions),
            "issues": issues,
            "suggestions": improvement_suggestions,
        }

        logger.debug("EvaluationAgent result: %s", result)
        return result

    def _compute_evaluation_score(self, churn_score: float, confidence: float, actions: List[Dict[str, Any]]) -> float:
        high_priority_count = sum(1 for action in actions if action.get("priority") == "high")
        action_score = min(len(actions) * 0.1, 0.3)
        priority_score = min(high_priority_count * 0.1, 0.2)
        base_score = 0.3 + confidence * 0.4 + action_score + priority_score
        alignment_bonus = 0.1 if churn_score >= 0.5 else 0.0
        evaluation_score = round(max(min(base_score + alignment_bonus, 1.0), 0.0), 3)
        return evaluation_score

    def _detect_issues(
        self,
        churn_score: float,
        explanation: Dict[str, Any],
        recommendations: Dict[str, Any],
        evaluation_score: float,
    ) -> List[str]:
        issues: List[str] = []
        reasons = explanation.get("reasons", [])
        actions = recommendations.get("actions", [])
        confidence = recommendations.get("confidence", 0.0)

        if not actions:
            issues.append("No retention recommendations were generated.")

        if confidence < 0.5:
            issues.append("Recommendation confidence is low.")

        if churn_score >= 0.8 and not any(action.get("priority") == "high" for action in actions):
            issues.append("High churn risk should include at least one high-priority action.")

        if not reasons:
            issues.append("Churn explanation is insufficient to justify the recommendations.")

        if evaluation_score < 0.5:
            issues.append("Overall recommendation evaluation score is below threshold.")

        return issues

    def _suggest_improvements(self, issues: List[str]) -> List[str]:
        suggestions: List[str] = []

        for issue in issues:
            if "No retention recommendations" in issue:
                suggestions.append("Enrich the reasoning agent to generate fallback recommendations for edge cases.")
            elif "confidence is low" in issue:
                suggestions.append("Improve churn scoring and explanation detail to increase recommendation confidence.")
            elif "high churn risk" in issue:
                suggestions.append("Add stronger escalation actions for high-risk customers.")
            elif "explanation is insufficient" in issue:
                suggestions.append("Enhance explanation rules with more customer-specific risk drivers.")
            elif "evaluation score is below threshold" in issue:
                suggestions.append("Review the evaluation criteria and adjust recommendation logic to improve alignment.")
            else:
                suggestions.append("Review recommendation output and business rules for better alignment.")

        return suggestions

    def _assess_alignment(self, churn_score: float, actions: List[Dict[str, Any]]) -> str:
        if churn_score >= 0.8:
            return "high" if any(action.get("priority") == "high" for action in actions) else "moderate"
        if churn_score >= 0.5:
            return "moderate"
        return "low"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.evaluate(
            context.get("customer", {}),
            context.get("recommendations", {}),
            context.get("churn_score", 0.0),
            context.get("explanation", {}),
        )
