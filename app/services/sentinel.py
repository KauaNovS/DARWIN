from typing import Dict, Any
from datetime import datetime, timedelta
from app.core.database import get_redis

class OnboardingSentinel:
    """
    Fase Feto: Primeiros 7 dias, Darwin age apenas como Diário Sentinela.
    Só libera complexidade quando a confiança é alta.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.phase_key = f"onboarding:phase:{user_id}"
    
    async def get_phase(self) -> str:
        """Retorna a fase atual do usuário."""
        phase = await self.redis.get(self.phase_key)
        if not phase:
            return "FETUS"  # Padrão
        return phase.decode()
    
    async def advance_phase(self, days_active: int, avg_energy: float):
        """Avança a fase baseado no comportamento."""
        phase = await self.get_phase()
        
        if phase == "FETUS" and days_active >= 7 and avg_energy > 0.6:
            await self.redis.setex(self.phase_key, 86400 * 365, "INFANT")
            return {"phase": "INFANT", "unlocked": ["tarefas_prioridade", "grafo_simples"]}
        
        elif phase == "INFANT" and days_active >= 30 and avg_energy > 0.7:
            await self.redis.setex(self.phase_key, 86400 * 365, "ADULT")
            return {"phase": "ADULT", "unlocked": ["agentes", "automacoes", "sequencias_completas"]}
        
        return {"phase": phase}
