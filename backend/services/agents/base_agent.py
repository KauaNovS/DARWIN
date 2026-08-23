# services/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Classe base para todos os agentes"""
    
    def __init__(self, name: str, user_id: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.user_id = user_id
        self.config = config or {}
        self.memory = {}
        self.status = "idle"
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a função principal do agente"""
        pass
    
    async def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa o contexto antes de agir"""
        return {
            "agent": self.name,
            "context": context,
            "analysis": {"status": "analyzed"}
        }
    
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Aprende com o feedback"""
        self.memory["last_feedback"] = feedback
        self.memory["feedback_count"] = self.memory.get("feedback_count", 0) + 1
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do agente"""
        return {
            "name": self.name,
            "status": self.status,
            "memory_count": len(self.memory),
            "config": self.config
        }
    
    def _log(self, message: str, level: str = "info") -> None:
        """Loga uma mensagem"""
        log_func = getattr(logger, level, logger.info)
        log_func(f"[{self.name}] {message}")
