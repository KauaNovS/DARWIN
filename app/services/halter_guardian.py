from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.database import get_redis
from app.models.stress import StressIndex

class HalterGuardian:
    """
    Halter: O Anjo da Guarda.
    Impõe pausa forçada se o Índice de Estresse ultrapassar o limiar.
    Bloqueia criação de novas tarefas em estado crítico.
    """
    
    CRITICAL_THRESHOLD = 0.75
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.lock_key = f"halter:lock:{user_id}"
    
    async def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia se o Halter deve atuar."""
        # Coleta sinais
        sleep_score = context.get("sleep_quality", 0.5)  # 0 a 1
        anxiety_score = context.get("anxiety", 0.5)
        workload_score = context.get("workload", 0.5)  # % de capacidade usada
        
        # Calcula Índice de Estresse (Quanto menor sleep, maior stress. Quanto maior anxiety/workload, maior stress)
        stress = ( (1 - sleep_score) * 0.4 ) + (anxiety_score * 0.3) + (workload_score * 0.3)
        stress = round(min(stress, 1.0), 3)
        
        # Salva no Redis para monitoramento
        await self.redis.setex(f"stress:{self.user_id}", 3600, stress)
        
        if stress >= self.CRITICAL_THRESHOLD:
            # Ativa o bloqueio
            await self.redis.setex(self.lock_key, 14400, "LOCKED")  # 4 horas de pausa forçada
            return {
                "status": "HALTER_ACTIVATED",
                "stress_index": stress,
                "message": "⚠️ Zona de Recuperação imposta por 4 horas. Novas tarefas bloqueadas.",
                "recovery_suggestions": [
                    "Dormir pelo menos 7 horas",
                    "Desconectar de estímulos digitais",
                    "Atividade física leve"
                ]
            }
        
        return {
            "status": "NORMAL",
            "stress_index": stress,
            "message": "Operação permitida."
        }
    
    async def can_create_task(self) -> bool:
        """Verifica se o usuário pode criar novas tarefas."""
        status = await self.redis.get(self.lock_key)
        return status != b"LOCKED"
