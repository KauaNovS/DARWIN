# services/instinct/genetic_memory.py
#
# CORRIGIDO:
# (1) importava de `app.core.database` / `app.models.genome` (inexistentes)
#     — usa `core.database.get_neo4j_driver()` / `get_redis()` deste backend.
# (2) chamava `await result.fetch()` num Result assíncrono do driver oficial
#     do Neo4j — esse método não existe na API async (`neo4j` >= 5). A forma
#     correta de consumir um `AsyncResult` é iterar com `async for`, então
#     trocamos por `[record async for record in result]`.
import json
from typing import Dict, Any
from datetime import datetime
from core.database import get_neo4j_driver, get_redis


class GeneticMemory:
    """
    Destila 30 dias de nós do grafo em um JSON de traços (DNA).
    O grafo ativo nunca fica poluído com histórico antigo.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.driver = get_neo4j_driver()
        self.redis = get_redis()
        self.genome_key = f"genome:{user_id}"

    async def distill(self) -> Dict[str, Any]:
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (n:Node {user_id: $user_id})
                WHERE n.created_at > datetime() - duration('P30D')
                RETURN n.name as name, n.type as type, n.intensity as intensity,
                       n.context as context, n.created_at as created_at
                LIMIT 1000
                """,
                user_id=self.user_id,
            )
            raw_events = [record async for record in result]

        if not raw_events:
            return {
                "genome": [],
                "traits_count": 0,
                "compressed": False,
                "message": "Not enough data for compression",
            }

        emotions, sleep_quality, task_completion, energy_levels = [], [], [], []

        for record in raw_events:
            node_type = record["type"]
            intensity = float(record["intensity"]) if record["intensity"] is not None else 0.5
            if node_type == "emotion":
                emotions.append(intensity)
            elif node_type == "sleep":
                sleep_quality.append(intensity)
            elif node_type == "task":
                task_completion.append(intensity)
            elif node_type == "energy":
                energy_levels.append(intensity)

        traits = []

        if emotions:
            avg_emotion = sum(emotions) / len(emotions)
            traits.append({
                "name": "emotional_stability",
                "value": round(1 - avg_emotion, 3),
                "confidence": round(min(len(emotions) / 30, 0.9), 3),
            })
        else:
            traits.append({"name": "emotional_stability", "value": 0.5, "confidence": 0.1})

        frequency = len(raw_events) / 30
        traits.append({
            "name": "behavioral_consistency",
            "value": round(min(frequency / 3, 1.0), 3),
            "confidence": round(min(len(raw_events) / 50, 0.9), 3),
        })

        if sleep_quality:
            traits.append({
                "name": "sleep_resilience",
                "value": round(sum(sleep_quality) / len(sleep_quality), 3),
                "confidence": round(min(len(sleep_quality) / 20, 0.9), 3),
            })
        else:
            traits.append({"name": "sleep_resilience", "value": 0.5, "confidence": 0.1})

        if energy_levels:
            traits.append({
                "name": "vital_energy",
                "value": round(sum(energy_levels) / len(energy_levels), 3),
                "confidence": round(min(len(energy_levels) / 20, 0.9), 3),
            })
        else:
            traits.append({"name": "vital_energy", "value": 0.5, "confidence": 0.1})

        if task_completion:
            traits.append({
                "name": "task_completion_rate",
                "value": round(sum(task_completion) / len(task_completion), 3),
                "confidence": round(min(len(task_completion) / 20, 0.9), 3),
            })
        else:
            traits.append({"name": "task_completion_rate", "value": 0.5, "confidence": 0.1})

        genome_payload = {
            "traits": traits,
            "traits_count": len(traits),
            "last_compressed_at": datetime.utcnow().isoformat(),
            "raw_events_archived": len(raw_events),
        }
        await self.redis.setex(self.genome_key, 86400 * 7, json.dumps(genome_payload))

        # Arquiva os nós brutos com mais de 30 dias (mantém o grafo ativo enxuto)
        async with self.driver.session() as session:
            await session.run(
                """
                MATCH (n:Node {user_id: $user_id})
                WHERE n.created_at < datetime() - duration('P30D')
                SET n:Archived
                REMOVE n:Node
                """,
                user_id=self.user_id,
            )

        return {
            "genome": traits,
            "traits_count": len(traits),
            "compressed": True,
            "message": "Genetic compression completed successfully",
        }

    async def get_genome(self) -> Dict[str, Any]:
        cached = await self.redis.get(self.genome_key)
        if cached:
            return json.loads(cached)
        return await self.distill()
