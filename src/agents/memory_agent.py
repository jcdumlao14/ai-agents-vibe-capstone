import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.config.logger import logger


class MemoryAgent:
    """Memory agent for storing and retrieving session context and interaction history."""

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, customer_id: str, customer_context: Dict[str, Any]) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "customer_id": customer_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "customer_context": customer_context,
            "interactions": [],
        }
        logger.debug("Created memory session %s for customer_id=%s", session_id, customer_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = self.sessions.get(session_id)
        logger.debug("Retrieved session %s: %s", session_id, bool(session))
        return session

    def append_interaction(self, session_id: str, event: Dict[str, Any]) -> None:
        session = self.sessions.get(session_id)
        if not session:
            logger.warning("Memory append attempted on missing session %s", session_id)
            return

        session["interactions"].append({
            "timestamp": datetime.utcnow().isoformat(),
            **event,
        })
        session["last_updated"] = datetime.utcnow().isoformat()
        logger.debug("Appended interaction to session %s", session_id)

    def query_recent_interactions(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        session = self.sessions.get(session_id)
        if not session:
            logger.warning("Memory query attempted on missing session %s", session_id)
            return []
        return session["interactions"][-limit:]

    def update_context(self, session_id: str, updates: Dict[str, Any]) -> None:
        session = self.sessions.get(session_id)
        if not session:
            logger.warning("Memory update attempted on missing session %s", session_id)
            return

        session["customer_context"].update(updates)
        session["last_updated"] = datetime.utcnow().isoformat()
        logger.debug("Updated context for session %s", session_id)

    def delete_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.debug("Deleted memory session %s", session_id)
        else:
            logger.warning("Attempted to delete missing session %s", session_id)
