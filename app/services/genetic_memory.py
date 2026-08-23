import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.models.genome import Genome
from app.core.database import get_neo4j_driver

class GeneticMemory:
    """
    Destila 30 dias em um JSON de 50 traços (DNA).
    O grafo ativo nunca fica poluído.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.driver = get_neo4j_driver()
    
    async def distill(self) -> Dict[str, Any]:
        """Processa os eventos do mês e gera o Genoma."""
        # 1. Busca eventos brutos do último mês (limitado a 1000)
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (n:Node {user_id: $user_id})
                WHERE n.created_at > datetime() - duration('P30D')
                RETURN n.name as name, n.type as type, n.intensity as intensity, 
                       n.context as context, n.created_at as created_at
                LIMIT 1000
                """,
                user_id=self.user_id
            )
            raw_events = await result.fetch()
        
        if not raw_events:
            return {"genome": {"traits": []}, "message": "Not enough data"}
        
        # 2. Extrai Traços (Simulação de ML)
        traits = []
        emotions = []
        sleep_quality = []
        
        for record in raw_events:
            node = record.data()
            if node['type'] == 'emotion':
                emotions.append(node['intensity'])
            if node['type'] == 'sleep':
                sleep_quality.append(node['intensity'])
        
        # Traço 1: Média Emocional
        if emotions:
            traits.append({"name": "emotional_stability", "value": round(1 - (sum(emotions)/len(emotions)), 2)})
        else:
            traits.append({"name": "emotional_stability", "value": 0.5})
        
        # Traço 2: Disciplina (frequência de registros)
        frequency = len(raw_events) / 30
        traits.append({"name": "behavioral_consistency", "value": round(min(frequency / 3, 1.0), 2)})
        
        # Traço 3: Sono (se disponível)
        if sleep_quality:
            traits.append({"name": "sleep_resilience", "value": round(sum(sleep_quality)/len(sleep_quality), 2)})
        else:
            traits.append({"name": "sleep_resilience", "value": 0.5})
        
        # 3. Salva o Genoma no Neo4j (substitui o antigo)
        await session.run(
            """
            MERGE (g:Genome {user_id: $user_id})
            SET g.traits = $traits,
                g.updated_at = datetime(),
                g.compress_count = g.compress_count + 1
            """,
            user_id=self.user_id,
            traits=json.dumps(traits)
        )
        
        # 4. Limpa os nós brutos antigos para manter o grafo leve (arquiva)
        await session.run(
            """
            MATCH (n:Node {user_id: $user_id})
            WHERE n.created_at < datetime() - duration('P30D')
            SET n:Archived
            REMOVE n:Node
            """,
            user_id=self.user_id
        )
        
        return {"genome": traits, "traits_count": len(traits), "compressed": True}
