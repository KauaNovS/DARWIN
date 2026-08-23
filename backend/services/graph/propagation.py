# services/graph/propagation.py
#
# NOTE: Referenced only implicitly in the plan (never defined). Wraps
# RelationManager.propagate() with a class name matching what the rest of
# the plan implies ("PropagationAnalyzer").
from typing import Any, Dict, List
from services.graph.relation_manager import RelationManager


class PropagationAnalyzer:
    """Analisa como o impacto se propaga pelo grafo a partir de um nó"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.relations = RelationManager(user_id)

    async def analyze(self, source_id: str, depth: int = 3) -> List[Dict[str, Any]]:
        return await self.relations.propagate(source_id, depth)
