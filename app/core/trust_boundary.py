from typing import Dict, Any
from app.core.database import get_redis

class TrustBoundary:
    """
    Níveis de Autonomia.
    Confiança > 90% -> Executa automático.
    Confiança > 50% -> Executa com notificação leve.
    Confiança < 50% -> Pergunta.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
    
    async def get_confidence(self, action_type: str) -> float:
        """Calcula a confiança para um tipo específico de ação."""
        key = f"trust:{self.user_id}:{action_type}"
        # Na prática, isso viria de um modelo de ML que avalia acertos anteriores.
        # Mock: baseado no histórico de aprovação do usuário.
        approval_rate = await self.redis.get(f"trust:history:{action_type}")
        if not approval_rate:
            return 0.6  # Confiança inicial média
        
        return float(approval_rate)
    
    async def execute_or_ask(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Decide entre executar ou perguntar."""
        confidence = await self.get_confidence(action.get("type", "default"))
        
        if confidence >= 0.9:
            return {"decision": "EXECUTE_AUTO", "confidence": confidence, "rollback_token": "..."}
        elif confidence >= 0.5:
            return {"decision": "EXECUTE_NOTIFY", "confidence": confidence, "message": "Ajustei sua rotina. Desfazer em 1 toque."}
        else:
            return {"decision": "ASK_USER", "confidence": confidence, "question": "Posso fazer isso por você?"}
    
    async def record_feedback(self, action_type: str, user_approved: bool):
        """Registra feedback para ajustar a confiança."""
        key = f"trust:history:{action_type}"
        await self.redis.lpush(key, 1 if user_approved else 0)
        await self.redis.ltrim(key, 0, 99)
        
        total = [int(x) for x in await self.redis.lrange(key, 0, -1)]
        new_rate = sum(total) / len(total) if total else 0.5
        await self.redis.setex(f"trust:{self.user_id}:{action_type}", 86400, new_rate)
