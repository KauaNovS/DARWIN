# services/instinct/halter_guardian.py
#
# CORRIGIDO: importava de `app.core.database` e `app.models.stress`
# (nenhum dos dois existe neste repositório). Usa `core.database.get_redis()`
# e `models.stress.StressIndex` (só documenta o formato, não é usado como
# tabela).
from typing import Dict, Any
from datetime import datetime
from core.database import get_redis


class HalterGuardian:
    """
    Halter: o Anjo da Guarda.
    Impõe pausa forçada se o Índice de Estresse ultrapassar o limiar.
    Bloqueia criação de novas tarefas em estado crítico.
    """

    CRITICAL_THRESHOLD = 0.75
    RECOVERY_DURATION_HOURS = 4

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.lock_key = f"halter:lock:{user_id}"
        self.stress_key = f"stress:{user_id}"
        self.history_key = f"stress:history:{user_id}"

    async def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        sleep_score = min(1.0, max(0.0, context.get("sleep_quality", 0.5)))
        anxiety_score = min(1.0, max(0.0, context.get("anxiety", 0.5)))
        workload_score = min(1.0, max(0.0, context.get("workload", 0.5)))

        stress = ((1 - sleep_score) * 0.4) + (anxiety_score * 0.3) + (workload_score * 0.3)
        stress = round(min(stress, 1.0), 3)

        await self.redis.setex(self.stress_key, 3600, str(stress))
        await self.redis.lpush(self.history_key, f"{datetime.utcnow().isoformat()}:{stress}")
        await self.redis.ltrim(self.history_key, 0, 999)

        if stress >= self.CRITICAL_THRESHOLD:
            await self.redis.setex(self.lock_key, self.RECOVERY_DURATION_HOURS * 3600, "LOCKED")
            return {
                "status": "HALTER_ACTIVATED",
                "stress_index": stress,
                "threshold": self.CRITICAL_THRESHOLD,
                "recovery_duration_hours": self.RECOVERY_DURATION_HOURS,
                "message": f"Zona de Recuperação imposta por {self.RECOVERY_DURATION_HOURS}h. Novas tarefas bloqueadas.",
                "recovery_suggestions": [
                    "Dormir pelo menos 7 horas",
                    "Desconectar de estímulos digitais por 1 hora",
                    "Atividade física leve (caminhada)",
                    "Respiração profunda (5 minutos)",
                ],
            }

        return {
            "status": "NORMAL",
            "stress_index": stress,
            "threshold": self.CRITICAL_THRESHOLD,
            "message": "Operação permitida.",
        }

    async def can_create_task(self) -> bool:
        status = await self.redis.get(self.lock_key)
        return status != "LOCKED"

    async def get_current_stress(self) -> float:
        value = await self.redis.get(self.stress_key)
        return float(value) if value else 0.0

    async def get_stress_history(self, limit: int = 30) -> list:
        values = await self.redis.lrange(self.history_key, 0, limit - 1)
        return [v.split(":") for v in values] if values else []
