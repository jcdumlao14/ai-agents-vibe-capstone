import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.config.logger import logger
from src.agents.tool_agent import ToolAgent
from src.agents.reasoning_agent import ReasoningAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.reflection_agent import ReflectionAgent
from src.agents.logging_agent import LoggingAgent


@dataclass
class EvaluationMetrics:
    accuracy: Optional[float] = None
    latency_seconds: Optional[float] = None
    tool_calls: int = 0
    memory_usage: Optional[int] = None
    reasoning_depth: Optional[int] = None
    cost_estimate: Optional[float] = None
    token_usage: Optional[int] = None
    hallucinations: List[str] = field(default_factory=list)
    business_kpis: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class EvaluationFramework:
    """Framework for measuring multi-agent performance and business outcomes."""

    def __init__(self):
        self.tool_agent = ToolAgent()
        self.reasoning_agent = ReasoningAgent()
        self.memory_agent = MemoryAgent()
        self.evaluation_agent = EvaluationAgent()
        self.reflection_agent = ReflectionAgent()
        self.logging_agent = LoggingAgent()

    def evaluate_customer_run(self, customer: Dict[str, Any], expected_score: Optional[float] = None) -> EvaluationMetrics:
        logger.info("EvaluationFramework: starting evaluation run for customer_id=%s", customer.get("customer_id"))

        metrics = EvaluationMetrics()
        start = time.perf_counter()

        session_id = self.memory_agent.create_session(customer.get("customer_id", "unknown"), customer)
        metrics.memory_usage = self._estimate_memory_usage(customer)

        tool_result = self.tool_agent.call_tool("model_inference", {"customer": customer})
        metrics.tool_calls += 1
        if tool_result["status"] == "success" and tool_result["tool"] == "model_inference":
            metrics.accuracy = self._compute_accuracy(tool_result["result"].get("churn_score"), expected_score)

        churn_score = tool_result["result"].get("churn_score", 0.5)
        explanation = self._explain_churn(customer, churn_score)
        recommendations = self.reasoning_agent.generate_recommendations(customer, churn_score, explanation)
        metrics.reasoning_depth = self._estimate_reasoning_depth(recommendations)

        evaluation = self.evaluation_agent.evaluate(customer, recommendations, churn_score, explanation)
        metrics.issues.extend(evaluation.get("issues", []))
        metrics.suggestions.extend(evaluation.get("suggestions", []))

        reflection = self.reflection_agent.reflect({
            "churn_score": churn_score,
            "explanation": explanation,
            "recommendations": recommendations,
        })

        logging_metrics = {
            "session_id": session_id,
            "tool_status": tool_result["status"],
            "churn_score": churn_score,
            "evaluation_score": evaluation["evaluation_score"],
            "gravity_index": tool_result["result"].get("gravity_index"),
        }
        self.logging_agent.log_metrics(logging_metrics)

        elapsed = time.perf_counter() - start
        metrics.latency_seconds = round(elapsed, 3)
        metrics.token_usage = self._estimate_token_usage(customer, recommendations, explanation, reflection)
        metrics.cost_estimate = self._estimate_cost(metrics.token_usage, tool_result, recommendations)
        metrics.business_kpis = self._compute_business_kpis(customer, churn_score, recommendations, evaluation)

        self.memory_agent.append_interaction(session_id, {
            "event": "evaluation_run",
            "metrics": metrics.__dict__,
            "evaluation": evaluation,
            "reflection": reflection,
        })

        logger.info("EvaluationFramework completed for session_id=%s", session_id)
        return metrics

    def _compute_accuracy(self, predicted: Optional[float], expected: Optional[float]) -> Optional[float]:
        if predicted is None or expected is None:
            return None
        return round(1.0 - abs(predicted - expected), 3)

    def _estimate_memory_usage(self, customer: Dict[str, Any]) -> int:
        return len(str(customer).encode("utf-8"))

    def _estimate_reasoning_depth(self, recommendations: Dict[str, Any]) -> int:
        return len(recommendations.get("actions", []))

    def _estimate_token_usage(self, customer: Dict[str, Any], recommendations: Dict[str, Any], explanation: Dict[str, Any], reflection: Dict[str, Any]) -> int:
        total_chars = len(str(customer)) + len(str(recommendations)) + len(str(explanation)) + len(str(reflection))
        return max(int(total_chars / 4), 1)

    def _estimate_cost(self, token_usage: int, tool_result: Dict[str, Any], recommendations: Dict[str, Any]) -> float:
        base_cost = token_usage * 0.00002
        external_cost = 0.0
        if tool_result["result"].get("source") == "google_adk":
            external_cost += 0.01
        if tool_result["result"].get("source") == "google_antigravity":
            external_cost += 0.015
        return round(base_cost + external_cost + len(recommendations.get("actions", [])) * 0.002, 4)

    def _compute_business_kpis(self, customer: Dict[str, Any], churn_score: float, recommendations: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
        actions = recommendations.get("actions", [])
        expected_retention = round(1.0 - churn_score, 3)
        customer_health = "high" if churn_score < 0.35 else "medium" if churn_score < 0.7 else "low"
        churn_action_rate = round(len([a for a in actions if a.get("priority") in ("high", "medium")]) / max(len(actions), 1), 3)
        return {
            "expected_retention_rate": expected_retention,
            "customer_health": customer_health,
            "churn_action_rate": churn_action_rate,
            "evaluation_score": evaluation["evaluation_score"],
        }

    def _explain_churn(self, customer: Dict[str, Any], churn_score: float) -> Dict[str, Any]:
        reasons = []
        if customer.get("usage", 0) < 30:
            reasons.append("Low product usage")
        if customer.get("support_tickets", 0) > 2:
            reasons.append("Frequent support issues")
        if customer.get("contract_months_remaining", 0) < 2:
            reasons.append("Near contract renewal")
        if not reasons:
            reasons.append("No critical churn drivers identified")
        return {"churn_score": churn_score, "reasons": reasons}
