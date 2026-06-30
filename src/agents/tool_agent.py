import time
from typing import Any, Callable, Dict, List, Optional

from src.config.logger import logger
from src.integrations.google_adk import GoogleADKIntegration
from src.integrations.google_antigravity import GoogleAntigravityIntegration


class ToolAgent:
    """Tool agent for executing external operations and service calls."""

    def __init__(self):
        self.name = "BusinessPilot Tool Agent"
        self.version = "0.1.0"
        self.google_adk = GoogleADKIntegration()
        self.google_antigravity = GoogleAntigravityIntegration()
        self.tools: Dict[str, Callable[..., Any]] = {
            "model_inference": self._model_inference_tool,
            "google_adk_inference": self._google_adk_inference_tool,
            "google_antigravity_analysis": self._google_antigravity_tool,
            "data_store_read": self._data_store_read_tool,
            "crm_notification": self._crm_notification_tool,
        }
        self.max_retries = 3
        self.retry_delay = 1.0

    def call_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("ToolAgent calling tool '%s' with payload: %s", tool_name, payload)

        tool = self.tools.get(tool_name)
        if tool is None:
            logger.error("ToolAgent missing tool: %s", tool_name)
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
            }

        attempt = 0
        while attempt < self.max_retries:
            try:
                result = tool(payload)
                logger.info("ToolAgent tool '%s' succeeded", tool_name)
                return {
                    "status": "success",
                    "tool": tool_name,
                    "result": result,
                }
            except Exception as exc:
                attempt += 1
                logger.warning(
                    "ToolAgent tool '%s' failed on attempt %s: %s",
                    tool_name,
                    attempt,
                    exc,
                )
                if attempt >= self.max_retries:
                    logger.error("ToolAgent tool '%s' exhausted retries", tool_name)
                    return self._fallback_response(tool_name, payload, exc)
                time.sleep(self.retry_delay)

    def _fallback_response(self, tool_name: str, payload: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        logger.debug("ToolAgent fallback activated for tool '%s'", tool_name)
        return {
            "status": "fallback",
            "tool": tool_name,
            "message": f"Fallback response for tool '{tool_name}' due to: {error}",
            "result": self._default_tool_response(tool_name, payload),
        }

    def _default_tool_response(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "model_inference":
            return {"churn_score": 0.5, "explanation": ["Default fallback score"]}
        if tool_name == "data_store_read":
            return {"data": {}, "note": "Default empty data response"}
        if tool_name == "crm_notification":
            return {"notified": False, "note": "CRM call skipped due to fallback"}
        return {"note": "No fallback available"}

    def _model_inference_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        customer = payload.get("customer", {})
        if self.google_adk.is_enabled():
            try:
                return self._google_adk_inference_tool(payload)
            except Exception as exc:
                logger.warning("Google ADK inference failed, falling back to local model: %s", exc)

        usage = customer.get("usage", 0)
        support_tickets = customer.get("support_tickets", 0)
        score = min(max((1.0 - usage / 100.0) + support_tickets * 0.05, 0.0), 1.0)
        return {"churn_score": round(score, 3), "source": "local_heuristic"}

    def _google_adk_inference_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        customer = payload.get("customer", {})
        prediction = self.google_adk.predict_customer_churn(customer)
        return prediction

    def _google_antigravity_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        customer = payload.get("customer", {})
        analysis = self.google_antigravity.analyze_customer(customer)
        return analysis

    def _data_store_read_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        key = payload.get("key")
        return {"key": key, "data": {}, "note": "Data store read placeholder"}

    def _crm_notification_tool(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = payload.get("customer_id")
        return {"customer_id": customer_id, "notified": True, "status": "queued"}
