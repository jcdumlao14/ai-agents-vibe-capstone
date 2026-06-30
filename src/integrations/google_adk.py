from typing import Any, Dict, List, Optional

from google.cloud import aiplatform

from src.config.logger import logger
from src.config.settings import settings


class GoogleADKIntegration:
    """Google ADK integration wrapper for Vertex AI prediction."""

    def __init__(self):
        self.name = "BusinessPilot Google ADK Integration"
        self.version = "0.1.0"
        self.initialized = False

    def is_enabled(self) -> bool:
        return bool(settings.use_google_adk and settings.google_adk_endpoint_id)

    def initialize(self) -> None:
        if self.initialized:
            return
        if not self.is_enabled():
            raise RuntimeError("Google ADK integration is not configured")

        aiplatform.init(
            project=settings.google_project_id,
            location=settings.google_region,
        )
        self.initialized = True
        logger.debug("Google ADK initialized for project=%s region=%s", settings.google_project_id, settings.google_region)

    def predict(self, instances: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.initialize()
        endpoint_name = settings.google_adk_endpoint_id
        logger.info("GoogleADKIntegration sending prediction request to endpoint=%s", endpoint_name)

        endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
        response = endpoint.predict(instances=instances)

        predictions = []
        if hasattr(response, "predictions"):
            for prediction in response.predictions:
                if hasattr(prediction, "to_dict"):
                    predictions.append(prediction.to_dict())
                else:
                    predictions.append(prediction)
        else:
            predictions = [response]

        return {
            "predictions": predictions,
            "deployed_model_id": getattr(response, "deployed_model_id", None),
        }

    def extract_churn_score(self, prediction: Dict[str, Any]) -> Optional[float]:
        predictions = prediction.get("predictions", [])
        if not predictions:
            return None

        first = predictions[0]
        if isinstance(first, dict):
            for field in ("churn_score", "score", "prediction", "risk_score"):
                value = first.get(field)
                if isinstance(value, (int, float)):
                    return float(value)
            for value in first.values():
                if isinstance(value, (int, float)):
                    return float(value)
        elif isinstance(first, (int, float)):
            return float(first)

        return None

    def predict_customer_churn(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.predict([customer])
            churn_score = self.extract_churn_score(response)
            if churn_score is None:
                raise ValueError("Google ADK response did not contain a churn score")

            return {
                "churn_score": round(churn_score, 3),
                "source": "google_adk",
                "raw_response": response,
            }
        except Exception as exc:
            logger.warning("Google ADK prediction failed: %s", exc)
            raise
