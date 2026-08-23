# services/agents/factory.py
from typing import Dict, Type
from services.agents.base_agent import BaseAgent
from services.agents.safira import SafiraAgent
from services.agents.atlas import AtlasAgent
from services.agents.orion import OrionAgent

class AgentFactory:
    """Fábrica de agentes"""
    
    _agents: Dict[str, Type[BaseAgent]] = {
        "safira": SafiraAgent,
        "atlas": AtlasAgent,
        "orion": OrionAgent,
    }
    
    @classmethod
    def create(cls, agent_name: str, user_id: str, config: Dict = None) -> BaseAgent:
        """Cria um agente pelo nome"""
        agent_class = cls._agents.get(agent_name.lower())
        if not agent_class:
            raise ValueError(f"Unknown agent: {agent_name}")
        return agent_class(user_id, config)
    
    @classmethod
    def get_available_agents(cls) -> list:
        """Retorna lista de agentes disponíveis"""
        return list(cls._agents.keys())
