from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from src.agents.main_agent import MainAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.planner_agent import PlannerAgent
from src.config.logger import logger
from src.config.settings import settings


class CustomerContext(BaseModel):
    customer_id: str
    usage: float = 0.0
    support_tickets: int = 0
    contract_months_remaining: int = 12


class MCPExecuteRequest(BaseModel):
    task: str = "score"
    session_id: str | None = None
    customer: CustomerContext | None = None


mcp_router = APIRouter(prefix="/mcp", tags=["mcp"])
main_agent = MainAgent()
planner_agent = PlannerAgent()
memory_agent = MemoryAgent()


@mcp_router.get("/status")
def mcp_status() -> Dict[str, Any]:
    return {
        "status": "ok",
        "server": "BusinessPilot MCP Server",
        "version": "0.1.0",
        "environment": settings.environment,
        "google_adk_enabled": settings.use_google_adk,
        "google_adk_endpoint": settings.google_adk_endpoint_id,
    }


@mcp_router.post("/execute")
def mcp_execute(request: MCPExecuteRequest) -> Dict[str, Any]:
    if request.session_id:
        session = memory_agent.get_session(request.session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        customer_data = session["customer_context"]
        session_id = request.session_id
    else:
        if request.customer is None:
            raise HTTPException(status_code=400, detail="Customer context is required when session_id is missing")
        session_id = memory_agent.create_session(request.customer.customer_id, request.customer.dict())
        customer_data = request.customer.dict()

    task = request.task.lower().strip()
    if task == "score":
        result = main_agent.run({"customer": customer_data})
    elif task == "plan":
        result = planner_agent.build_plan({"customer": customer_data})
    elif task == "full":
        plan = planner_agent.build_plan({"customer": customer_data})
        score = main_agent.run({"customer": customer_data})
        result = {"plan": plan, "score": score}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported MCP task: {request.task}")

    memory_agent.append_interaction(session_id, {"event": "mcp_execute", "task": task, "result": result})
    logger.info("MCP execute completed for session_id=%s task=%s", session_id, task)
    return {
        "status": "success",
        "session_id": session_id,
        "task": task,
        "result": result,
    }


@mcp_router.get("/session/{session_id}/interactions")
def mcp_session_interactions(session_id: str) -> Dict[str, Any]:
    session = memory_agent.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "customer_id": session["customer_id"],
        "interactions": session["interactions"],
    }
