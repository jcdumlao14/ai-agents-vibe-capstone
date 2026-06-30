from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agents.main_agent import MainAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.planner_agent import PlannerAgent
from src.config.logger import logger
from src.services.mcp_server import mcp_router


class CustomerContext(BaseModel):
    customer_id: str
    usage: float = 0.0
    support_tickets: int = 0
    contract_months_remaining: int = 12


class SessionRequest(CustomerContext):
    session_id: str | None = None


app = FastAPI(title="BusinessPilot AI API")
main_agent = MainAgent()
planner_agent = PlannerAgent()
memory_agent = MemoryAgent()
app.include_router(mcp_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/session")
def create_session(context: CustomerContext):
    try:
        session_id = memory_agent.create_session(context.customer_id, context.dict())
        return {"status": "success", "session_id": session_id}
    except Exception as exc:
        logger.exception("Failed to create memory session")
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.get("/session/{session_id}")
def get_session(session_id: str):
    session = memory_agent.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.post("/plan")
def plan_customer_retention(context: SessionRequest):
    try:
        customer_data = context.dict(exclude_none=True)
        if context.session_id:
            session = memory_agent.get_session(context.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            customer_data = session["customer_context"]
        result = planner_agent.build_plan({"customer": customer_data})
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        memory_agent.append_interaction(context.session_id or "", {"event": "plan_requested", "plan": result})
        return result
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to build retention plan")
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.post("/score")
def score_customer(context: SessionRequest):
    try:
        customer_data = context.dict(exclude_none=True)
        session_id = context.session_id
        if session_id:
            session = memory_agent.get_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            customer_data = session["customer_context"]
        else:
            session_id = memory_agent.create_session(context.customer_id, context.dict())

        result = main_agent.run({"customer": customer_data})
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))

        memory_agent.append_interaction(session_id, {"event": "score_requested", "result": result})
        return {"session_id": session_id, **result}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to score customer")
        raise HTTPException(status_code=500, detail="Internal server error") from exc
