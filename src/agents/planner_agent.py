from typing import Any, Dict, List

from src.config.logger import logger


class PlannerAgent:
    """Planner agent for constructing execution plans from business context."""

    def __init__(self):
        self.name = "BusinessPilot Planner Agent"
        self.version = "0.1.0"

    def build_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("PlannerAgent building plan for context: %s", context)

        customer = context.get("customer")
        if customer is None:
            logger.error("PlannerAgent missing customer information")
            return {
                "status": "error",
                "message": "customer context is required for planning",
            }

        plan = self._compose_plan(customer)
        summary = f"Plan composed with {len(plan)} task(s)."

        logger.info("PlannerAgent plan built successfully for customer_id=%s", customer.get("customer_id"))
        return {
            "status": "success",
            "plan": plan,
            "summary": summary,
            "fallback": self._needs_fallback(customer),
        }

    def _compose_plan(self, customer: Dict[str, Any]) -> List[Dict[str, Any]]:
        tasks = [
            {
                "id": "capture_context",
                "name": "Capture customer context",
                "description": "Validate and normalize customer profile data.",
                "depends_on": [],
            },
            {
                "id": "score_churn",
                "name": "Score churn risk",
                "description": "Compute churn probability from customer signals.",
                "depends_on": ["capture_context"],
            },
            {
                "id": "explain_risk",
                "name": "Explain churn drivers",
                "description": "Generate the business rationale behind the churn score.",
                "depends_on": ["score_churn"],
            },
            {
                "id": "recommend_retention",
                "name": "Recommend retention actions",
                "description": "Create targeted retention strategies based on risk and customer state.",
                "depends_on": ["explain_risk"],
            },
            {
                "id": "evaluate_plan",
                "name": "Evaluate recommendation plan",
                "description": "Validate recommendations against business rules and risk tolerance.",
                "depends_on": ["recommend_retention"],
            },
        ]

        if self._needs_fallback(customer):
            tasks.append({
                "id": "fallback_review",
                "name": "Fallback review",
                "description": "Use default retention guidance when the plan is incomplete.",
                "depends_on": ["evaluate_plan"],
            })

        return tasks

    def _needs_fallback(self, customer: Dict[str, Any]) -> bool:
        missing_fields = [
            key for key in ("usage", "support_tickets", "contract_months_remaining")
            if key not in customer
        ]
        needs_fallback = len(missing_fields) > 0
        if needs_fallback:
            logger.warning(
                "PlannerAgent fallback required due to missing fields: %s", missing_fields
            )
        return needs_fallback
