# services/graph/node_manager.py
from typing import Dict, Any, List, Optional
from neo4j import AsyncGraphDatabase
from core.database import get_neo4j_driver
import uuid

class NodeManager:
    """Gerencia nós do grafo relacional"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.driver = get_neo4j_driver()
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo nó"""
        node_id = str(uuid.uuid4())
        
        async with self.driver.session() as session:
            result = await session.run(
                """
                CREATE (n:Node {
                    id: $id,
                    user_id: $user_id,
                    name: $name,
                    type: $type,
                    description: $description,
                    context: $context,
                    intensity: $intensity,
                    weight: $weight,
                    status: $status,
                    created_at: datetime(),
                    updated_at: datetime()
                })
                RETURN n
                """,
                id=node_id,
                user_id=self.user_id,
                name=data.get("name", "Untitled"),
                type=data.get("type", "generic"),
                description=data.get("description", ""),
                context=json.dumps(data.get("context", {})),
                intensity=data.get("intensity", 1.0),
                weight=data.get("weight", 1.0),
                status=data.get("status", "active")
            )
            
            record = await result.single()
            return self._record_to_dict(record["n"])
    
    async def get(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Obtém um nó por ID"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (n:Node {id: $id, user_id: $user_id})
                RETURN n
                """,
                id=node_id,
                user_id=self.user_id
            )
            record = await result.single()
            return self._record_to_dict(record["n"]) if record else None
    
    async def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca nós por critérios"""
        # TODO: Implementar busca flexível
        pass
    
    async def get_relations(self, node_id: str) -> List[Dict[str, Any]]:
        """Obtém todas as relações de um nó"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (n:Node {id: $id, user_id: $user_id})
                OPTIONAL MATCH (n)-[r]-()
                RETURN n, r
                """,
                id=node_id,
                user_id=self.user_id
            )
            records = await result.fetch()
            return [self._record_to_dict(record) for record in records]
    
    def _record_to_dict(self, record) -> Dict[str, Any]:
        """Converte registro Neo4j para dict"""
        if not record:
            return {}
        return {
            "id": record.get("id"),
            "user_id": record.get("user_id"),
            "name": record.get("name"),
            "type": record.get("type"),
            "description": record.get("description"),
            "context": json.loads(record.get("context", "{}")),
            "intensity": record.get("intensity"),
            "weight": record.get("weight"),
            "status": record.get("status"),
            "created_at": record.get("created_at"),
            "updated_at": record.get("updated_at")
        }
