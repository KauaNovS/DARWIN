import asyncio
from typing import Dict, Any
from datetime import datetime
from app.core.database import get_redis

class EcoListener:
    """
    Módulo "Eco": Escuta passiva de comportamento (digitação, cancelamentos, tom).
    Inferência sem necessidade de registro manual.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.keys = {
            "typing_speed": f"eco:{user_id}:typing",
            "cancel_rate": f"eco:{user_id}:cancel",
            "hesitation": f"eco:{user_id}:hesitation"
        }
    
    async def feed_behavior(self, event_type: str, value: float):
        """Alimenta o Eco com dados comportamentais brutos."""
        if event_type == "typing":
            # Quanto mais devagar e com mais backspaces, maior o índice de hesitação
            await self.redis.lpush(self.keys["typing_speed"], value)
            await self.redis.ltrim(self.keys["typing_speed"], 0, 99)  # Mantém últimas 100
        
        elif event_type == "task_cancel":
            # Cancelação de tarefas = sobrecarga ou baixa energia
            await self.redis.lpush(self.keys["cancel_rate"], 1)
            await self.redis.ltrim(self.keys["cancel_rate"], 0, 49)
    
    async def infer_context(self) -> Dict[str, float]:
        """Inferência contextual implícita baseada no comportamento."""
        typing_speeds = [float(x) for x in await self.redis.lrange(self.keys["typing_speed"], 0, -1)]
        cancel_rates = [float(x) for x in await self.redis.lrange(self.keys["cancel_rate"], 0, -1)]
        
        # Indicadores
        cognitive_load = 0.5  # Neutro
        energy_level = 0.5
        
        if typing_speeds:
            avg_speed = sum(typing_speeds) / len(typing_speeds)
            # Se digitar muito devagar (< 30% da média histórica), indica fadiga
            cognitive_load = 0.2 if avg_speed > 1.0 else 0.8  # Simulação
        
        if cancel_rates:
            recent_cancels = sum(cancel_rates[:10]) if len(cancel_rates) > 10 else sum(cancel_rates)
            if recent_cancels > 3:  # Mais de 3 cancelamentos recentes
                energy_level = 0.2  # Baixa energia
        
        # Escreve o estado inferido no contexto "sombra" (não exige confirmação do user)
        return {
            "inferred_cognitive_load": cognitive_load,
            "inferred_energy": energy_level,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "eco_listener"
        }
