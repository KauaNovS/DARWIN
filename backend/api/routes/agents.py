# api/routes/agents.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from core.dependencies import get_current_user
from models.user import User
from services.agents.factory import AgentFactory

router = APIRouter()


class AgentInput(BaseModel):
    input_data: Dict[str, Any] = {}


@router.get("/")
async def list_agents():
    """Lista os agentes disponíveis (safira, atlas, orion)."""
    return {"agents": AgentFactory.get_available_agents()}


@router.post("/{agent_name}/execute")
async def execute_agent(
    agent_name: str,
    data: AgentInput,
    current_user: User = Depends(get_current_user),
):
    try:
        agent = AgentFactory.create(agent_name, str(current_user.id))
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Agente '{agent_name}' não existe")

    return await agent.execute(data.input_data)
