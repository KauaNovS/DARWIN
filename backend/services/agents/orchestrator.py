# services/agents/orchestrator.py
from typing import Dict, Any, List
from services.agents.factory import AgentFactory
from services.memory.live_memory import LiveMemory

class AgentOrchestrator:
    """Orquestra a execução de múltiplos agentes"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.agents = {}
        self.memory = LiveMemory(user_id)
    
    async def load_agents(self, agent_names: List[str]) -> None:
        """Carrega agentes pelo nome"""
        for name in agent_names:
            if name not in self.agents:
                self.agents[name] = AgentFactory.create(name, self.user_id)
    
    async def execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa um agente específico"""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent not loaded: {agent_name}")
        
        # Prepara contexto
        context = await self.memory.get_relevant_context(
            str(input_data)
        )
        
        # Executa agente
        result = await agent.execute(input_data)
        
        # Registra resultado na memória
        await self.memory.store({
            "type": "agent_execution",
            "data": {
                "agent": agent_name,
                "input": input_data,
                "result": result,
                "context": context
            }
        })
        
        return result
    
    async def execute_pipeline(self, pipeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executa um pipeline de agentes"""
        results = {}
        
        for step in pipeline:
            agent_name = step.get("agent")
            input_data = step.get("input", {})
            
            # Adiciona resultados anteriores ao contexto
            if results:
                input_data["previous_results"] = results
            
            result = await self.execute_agent(agent_name, input_data)
            results[agent_name] = result
        
        return results
