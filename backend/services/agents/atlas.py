# services/agents/atlas.py
#
# NOTE: Referenced by services/agents/factory.py but never implemented in the
# original plan document (only SafiraAgent was fully specified). This is a
# minimal stub following the same BaseAgent pattern so imports don't break —
# flesh out execute() with real logic for whatever Atlas is meant to do
# (the plan suggests something execution/project-oriented).
from typing import Any, Dict
from services.agents.base_agent import BaseAgent


class AtlasAgent(BaseAgent):
    """Agente de Execução/Projetos (stub — implementar lógica real)"""

    def __init__(self, user_id: str, config: Dict[str, Any] = None):
        super().__init__("Atlas", user_id, config or {"specialization": "execution"})

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: Implementar lógica real do Atlas (projetos, tarefas, execução)
        return {
            "agent": self.name,
            "status": "not_implemented",
            "received": input_data,
        }
