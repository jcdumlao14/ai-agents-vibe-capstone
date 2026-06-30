from typing import Any, Dict

from src.agents.evaluation_agent import EvaluationAgent
from src.agents.logging_agent import LoggingAgent
from src.agents.reasoning_agent import ReasoningAgent
from src.agents.reflection_agent import ReflectionAgent
from src.agents.tool_agent import ToolAgent
from src.config.logger import logger


class MainAgent:
    """Main orchestration agent for the BusinessPilot AI solution."""

    def __init__(self):
        self.name = "BusinessPilot Main Agent"
        self.version = "0.1.0"
        self.tool_agent = ToolAgent()
        self.reasoning_agent = ReasoningAgent()
        self.reflection_agent = ReflectionAgent()
        self.evaluation_agent = EvaluationAgent()
        self.logging_agent = LoggingAgent()

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("MainAgent started with context: %s", context)

        customer = context.get("customer")
        if customer is None:
            logger.error("Missing customer context")
            return {
                "status": "error",
                "message": "customer context is required",
            }

        score_result = self.tool_agent.call_tool("model_inference", {"customer": customer})
        if score_result["status"] != "success":
            logger.warning("ToolAgent returned fallback response for model_inference")

        churn_score = score_result["result"].get("churn_score", 0.5)
        explanation = self._explain_churn(customer, churn_score)
        recommendations = self.reasoning_agent.generate_recommendations(customer, churn_score, explanation)
        response = {
            "status": "success",
            "customer_id": customer.get("customer_id"),
            "churn_score": churn_score,
            "explanation": {**explanation, "tool_status": score_result["status"]},
            "recommendations": recommendations,
        }

        reflection = self.reflection_agent.reflect({
            "churn_score": churn_score,
            "explanation": response["explanation"],
            "recommendations": recommendations,
        })
        evaluation = self.evaluation_agent.evaluate(customer, recommendations, churn_score, response["explanation"])
        logging_outcome = self.logging_agent.audit({
            "customer": customer,
            "churn_score": churn_score,
            "explanation": response["explanation"],
            "recommendations": recommendations,
        })

        response["reflection"] = reflection
        response["evaluation"] = evaluation
        response["logging"] = logging_outcome

        logger.info("MainAgent completed successfully for customer_id=%s", customer.get("customer_id"))
        return response

    def _explain_churn(self, customer: Dict[str, Any], churn_score: float) -> Dict[str, Any]:
        logger.debug("Explaining churn score for customer_id=%s", customer.get("customer_id"))
        reasons = []

        if customer.get("usage", 0) < 30:
            reasons.append("Low product usage")
        if customer.get("support_tickets", 0) > 2:
            reasons.append("Frequent support issues")
        if customer.get("contract_months_remaining", 0) < 2:
            reasons.append("Near contract renewal")

        if not reasons:
            reasons.append("No critical churn drivers identified")

        return {
            "churn_score": churn_score,
            "reasons": reasons,
        }
