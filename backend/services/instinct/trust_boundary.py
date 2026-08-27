# services/instinct/trust_boundary.py
#
# CORRIGIDO: importava de `app.core.database`, um módulo que não existe
# neste repositório (era de um scaffold paralelo e desconectado). Agora usa
# `core.database.get_redis()`, que já é um cliente Redis assíncrono real
# testado neste backend.
from typing import Dict, Any
from core.database import get_redis


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
        key = f"trust:{self.user_id}:{action_type}"
        approval_rate = await self.redis.get(key)
        if not approval_rate:
            return 0.6
        return float(approval_rate)

    async def execute_or_ask(self, action: Dict[str, Any]) -> Dict[str, Any]:
        action_type = action.get("type", "default")
        confidence = await self.get_confidence(action_type)

        if confidence >= 0.9:
            return {
                "decision": "EXECUTE_AUTO",
                "confidence": confidence,
                "rollback_token": f"rollback_{action_type}_{self.user_id}",
            }
        elif confidence >= 0.5:
            return {
                "decision": "EXECUTE_NOTIFY",
                "confidence": confidence,
                "message": f"Ajustei sua {action_type}. Desfazer em 1 toque.",
                "rollback_token": f"rollback_{action_type}_{self.user_id}",
            }
        else:
            return {
                "decision": "ASK_USER",
                "confidence": confidence,
                "question": f"Posso fazer a ação '{action_type}' por você?",
            }

    async def record_feedback(self, action_type: str, user_approved: bool) -> float:
        key = f"trust:history:{action_type}"
        await self.redis.lpush(key, 1 if user_approved else 0)
        await self.redis.ltrim(key, 0, 99)

        raw = await self.redis.lrange(key, 0, -1)
        total = [int(x) for x in raw]
        new_rate = sum(total) / len(total) if total else 0.5
        await self.redis.setex(f"trust:{self.user_id}:{action_type}", 86400 * 7, str(new_rate))
        return new_rate
