import json
import urllib.request
from typing import Any, Dict

from src.config.logger import logger
from src.config.settings import settings


class GoogleAntigravityIntegration:
    """Google Antigravity integration wrapper for hypothetical cloud analysis."""

    def __init__(self):
        self.name = "BusinessPilot Google Antigravity Integration"
        self.version = "0.1.0"

    def is_enabled(self) -> bool:
        return bool(
            settings.use_google_antigravity
            and settings.google_antigravity_endpoint
            and settings.google_antigravity_api_key
        )

    def analyze(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_enabled():
            raise RuntimeError("Google Antigravity integration is not configured")

        request_payload = {
            "customer": customer,
            "project_id": settings.google_project_id,
            "metadata": {
                "source": "businesspilot",
                "environment": settings.environment,
            },
        }
        request_data = json.dumps(request_payload).encode("utf-8")

        request = urllib.request.Request(
            settings.google_antigravity_endpoint,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.google_antigravity_api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
                logger.info("Google Antigravity analysis completed successfully")
                return response_payload
        except Exception as exc:
            logger.warning("Google Antigravity request failed: %s", exc)
            raise

    def extract_gravity_index(self, analysis: Dict[str, Any]) -> float:
        gravity_index = analysis.get("gravity_index")
        if isinstance(gravity_index, (int, float)):
            return float(gravity_index)

        fallback_index = analysis.get("stability_score")
        if isinstance(fallback_index, (int, float)):
            return float(fallback_index)

        return 0.0

    def analyze_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        analysis = self.analyze(customer)
        gravity_index = self.extract_gravity_index(analysis)
        return {
            "gravity_index": round(gravity_index, 3),
            "analysis": analysis,
            "source": "google_antigravity",
        }
