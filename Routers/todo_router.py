from fastapi import APIRouter, HTTPException
from Agents.agent_todo import manager_agent
from Scheema.agent_request import AgentRequest
router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run")
async def run_agent(request: AgentRequest):
    try:
        result = manager_agent.run(request.instruction)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))