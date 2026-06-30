from typing import Any, Dict, List

from src.config.logger import logger


class ReflectionAgent:
    """Reflection agent to review output quality and generate improvement signals."""

    def __init__(self):
        self.name = "BusinessPilot Reflection Agent"
        self.version = "0.1.0"

    def reflect(self, execution_context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("ReflectionAgent reviewing execution context")

        observations = self._collect_observations(execution_context)
        issues = self._identify_issues(observations)
        improvements = self._suggest_improvements(observations)

        reflection = {
            "status": "completed",
            "observations": observations,
            "issues": issues,
            "recommended_improvements": improvements,
        }

        logger.debug("ReflectionAgent reflection result: %s", reflection)
        return reflection

    def _collect_observations(self, execution_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "churn_score": execution_context.get("churn_score"),
            "tool_status": execution_context.get("explanation", {}).get("tool_status"),
            "recommendation_count": len(execution_context.get("recommendations", {}).get("actions", [])),
            "reasons": execution_context.get("explanation", {}).get("reasons", []),
        }

    def _identify_issues(self, observations: Dict[str, Any]) -> List[str]:
        issues: List[str] = []

        if observations["tool_status"] != "success":
            issues.append("Tool fallback used for scoring")

        if observations["churn_score"] is None:
            issues.append("Missing churn score")

        if observations["recommendation_count"] == 0:
            issues.append("No retention recommendations generated")

        if not observations["reasons"]:
            issues.append("No explanation reasons were generated")

        return issues

    def _suggest_improvements(self, observations: Dict[str, Any]) -> List[str]:
        improvements: List[str] = []

        if observations["tool_status"] != "success":
            improvements.append("Improve model inference tool reliability or add a stronger fallback model.")

        if observations["churn_score"] is None:
            improvements.append("Ensure churn scoring output is always populated.")

        if observations["recommendation_count"] == 0:
            improvements.append("Expand retention reasoning logic to handle all customer segments.")

        if not observations["reasons"]:
            improvements.append("Add more explainability rules for churn drivers.")

        return improvements
