# services/instinct/eco_listener.py
#
# CORRIGIDO: importava de `app.core.database` (inexistente). Usa
# `core.database.get_redis()` deste backend.
from typing import Dict, Any
from datetime import datetime
from core.database import get_redis


class EcoListener:
    """
    Módulo "Eco": escuta passiva de comportamento (digitação, cancelamentos,
    hesitação). Inferência sem precisar de registro manual do usuário.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.keys = {
            "typing_speed": f"eco:{user_id}:typing",
            "typing_backspace": f"eco:{user_id}:backspace",
            "cancel_rate": f"eco:{user_id}:cancel",
            "hesitation": f"eco:{user_id}:hesitation",
        }

    async def feed_behavior(self, event_type: str, value: float) -> None:
        """Alimenta o Eco com dados comportamentais brutos."""
        if event_type == "typing":
            await self.redis.lpush(self.keys["typing_speed"], value)
            await self.redis.ltrim(self.keys["typing_speed"], 0, 99)
        elif event_type == "backspace":
            await self.redis.lpush(self.keys["typing_backspace"], value)
            await self.redis.ltrim(self.keys["typing_backspace"], 0, 99)
        elif event_type == "task_cancel":
            await self.redis.lpush(self.keys["cancel_rate"], 1)
            await self.redis.ltrim(self.keys["cancel_rate"], 0, 49)
        elif event_type == "hesitation":
            await self.redis.lpush(self.keys["hesitation"], value)
            await self.redis.ltrim(self.keys["hesitation"], 0, 49)

    async def infer_context(self) -> Dict[str, float]:
        """Inferência contextual implícita baseada no comportamento."""
        typing_speeds = [float(x) for x in await self.redis.lrange(self.keys["typing_speed"], 0, -1)]
        backspaces = [float(x) for x in await self.redis.lrange(self.keys["typing_backspace"], 0, -1)]
        cancel_rates = [float(x) for x in await self.redis.lrange(self.keys["cancel_rate"], 0, -1)]
        hesitations = [float(x) for x in await self.redis.lrange(self.keys["hesitation"], 0, -1)]

        cognitive_load = 0.5
        energy_level = 0.5
        focus_score = 0.5

        if typing_speeds:
            avg_speed = sum(typing_speeds) / len(typing_speeds)
            cognitive_load = max(0.1, min(0.9, 1.0 - (avg_speed / 100)))

        if backspaces:
            avg_backspace = sum(backspaces) / len(backspaces)
            cognitive_load = max(cognitive_load, min(0.9, avg_backspace / 10))

        if cancel_rates:
            recent_cancels = sum(cancel_rates[:10]) if len(cancel_rates) > 10 else sum(cancel_rates)
            energy_level = max(0.1, 1.0 - (recent_cancels / 20))

        if hesitations:
            avg_hesitation = sum(hesitations) / len(hesitations)
            focus_score = max(0.1, 1.0 - avg_hesitation)

        return {
            "inferred_cognitive_load": round(cognitive_load, 3),
            "inferred_energy": round(energy_level, 3),
            "inferred_focus": round(focus_score, 3),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "eco_listener",
        }

    async def get_behavior_summary(self) -> Dict[str, Any]:
        return {
            "typing_samples": await self.redis.llen(self.keys["typing_speed"]),
            "backspace_samples": await self.redis.llen(self.keys["typing_backspace"]),
            "cancel_samples": await self.redis.llen(self.keys["cancel_rate"]),
            "hesitation_samples": await self.redis.llen(self.keys["hesitation"]),
        }
