from typing import Any, Dict, List

from src.config.logger import logger


class ReasoningAgent:
    """Reasoning agent responsible for generating business-aligned retention recommendations."""

    def __init__(self):
        self.name = "BusinessPilot Reasoning Agent"
        self.version = "0.1.0"

    def generate_recommendations(
        self,
        customer: Dict[str, Any],
        churn_score: float,
        explanation: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info("ReasoningAgent generating recommendations for customer_id=%s", customer.get("customer_id"))

        actions = self._build_actions(customer, churn_score, explanation)
        confidence = self._estimate_confidence(churn_score, explanation)
        summary = self._create_summary(actions)

        logger.debug(
            "ReasoningAgent generated %s action(s) with confidence %s for customer_id=%s",
            len(actions),
            confidence,
            customer.get("customer_id"),
        )

        return {
            "actions": actions,
            "confidence": confidence,
            "summary": summary,
        }

    def _build_actions(
        self,
        customer: Dict[str, Any],
        churn_score: float,
        explanation: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        reasons = explanation.get("reasons", [])

        if churn_score >= 0.85:
            actions.append(self._action_template(
                "Executive risk review call",
                "high",
                "Very high churn risk requires executive attention.",
            ))

        if "Low product usage" in reasons:
            actions.append(self._action_template(
                "Activate usage re-engagement plan",
                "medium",
                "Improve adoption through targeted onboarding and coaching.",
            ))

        if "Frequent support issues" in reasons:
            actions.append(self._action_template(
                "Assign priority support case",
                "high",
                "Resolve operational issues and rebuild customer confidence.",
            ))

        if "Near contract renewal" in reasons:
            actions.append(self._action_template(
                "Prepare bespoke renewal offer",
                "medium",
                "Use incentives and contract flexibility to secure renewal.",
            ))

        if customer.get("industry") == "enterprise" and churn_score > 0.6:
            actions.append(self._action_template(
                "Engage customer success executive",
                "high",
                "Enterprise customers need tailored retention support.",
            ))

        if not actions:
            actions.append(self._action_template(
                "Monitor customer health and gather feedback",
                "low",
                "No immediate risk drivers were identified; continue observation.",
            ))

        return actions

    def _estimate_confidence(self, churn_score: float, explanation: Dict[str, Any]) -> float:
        reasons = explanation.get("reasons", [])
        base_confidence = churn_score if churn_score >= 0.5 else 0.5
        factor = 1.0 - min(len(reasons) * 0.1, 0.3)
        confidence = round(base_confidence * factor, 3)
        return max(min(confidence, 1.0), 0.0)

    def _create_summary(self, actions: List[Dict[str, Any]]) -> str:
        return f"Generated {len(actions)} recommended action(s) for retention."

    def _action_template(self, action: str, priority: str, rationale: str) -> Dict[str, Any]:
        return {
            "action": action,
            "priority": priority,
            "rationale": rationale,
        }
