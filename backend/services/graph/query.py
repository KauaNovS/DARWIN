# services/graph/query.py
#
# NOTE: Referenced only implicitly in the plan (never defined). Thin
# convenience wrapper around NodeManager/RelationManager for read queries.
from typing import Any, Dict, List
from services.graph.node_manager import NodeManager
from services.graph.relation_manager import RelationManager


class GraphQuery:
    """Consultas de leitura no grafo (stub — expandir conforme necessário)"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.nodes = NodeManager(user_id)
        self.relations = RelationManager(user_id)

    async def find_nodes(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        # TODO: Implementar filtros reais (delega no TODO do NodeManager.search)
        return await self.nodes.search(criteria)
