from typing import Any, Dict

from src.config.logger import logger


class LoggingAgent:
    """Logging agent for structured event capture and audit metadata."""

    def __init__(self):
        self.name = "BusinessPilot Logging Agent"
        self.version = "0.1.0"

    def log_event(self, event_name: str, payload: Dict[str, Any], level: str = "info") -> Dict[str, Any]:
        record = {
            "event": event_name,
            "payload": payload,
            "agent": self.name,
            "version": self.version,
        }

        if level == "debug":
            logger.debug("%s event=%s payload=%s", self.name, event_name, payload)
        elif level == "warning":
            logger.warning("%s event=%s payload=%s", self.name, event_name, payload)
        elif level == "error":
            logger.error("%s event=%s payload=%s", self.name, event_name, payload)
        else:
            logger.info("%s event=%s payload=%s", self.name, event_name, payload)

        return {"status": "logged", "record": record}

    def log_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("%s metrics=%s", self.name, metrics)
        return {"status": "metrics_logged", "metrics": metrics}

    def audit(self, context: Dict[str, Any]) -> Dict[str, Any]:
        customer = context.get("customer", {})
        churn_score = context.get("churn_score")
        recommendations = context.get("recommendations", {})
        reason_count = len(context.get("explanation", {}).get("reasons", []))
        action_count = len(recommendations.get("actions", []))

        audit = {
            "customer_id": customer.get("customer_id"),
            "churn_score": churn_score,
            "reason_count": reason_count,
            "action_count": action_count,
            "confidence": recommendations.get("confidence"),
            "tool_status": context.get("explanation", {}).get("tool_status"),
        }
        logger.info("%s audit summary=%s", self.name, audit)
        return {"status": "audited", "audit_summary": audit}

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.audit(context)
