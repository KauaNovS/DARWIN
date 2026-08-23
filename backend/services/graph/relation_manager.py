# services/graph/relation_manager.py
class RelationManager:
    """Gerencia relações do grafo relacional"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.driver = get_neo4j_driver()
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova relação"""
        relation_id = str(uuid.uuid4())
        
        async with self.driver.session() as session:
            # Verifica se os nós existem
            source = await self.driver.execute_query(
                "MATCH (n:Node {id: $id, user_id: $user_id}) RETURN n",
                id=data["source_id"], user_id=self.user_id
            )
            target = await self.driver.execute_query(
                "MATCH (n:Node {id: $id, user_id: $user_id}) RETURN n",
                id=data["target_id"], user_id=self.user_id
            )
            
            if not source or not target:
                raise ValueError("Source or target node not found")
            
            result = await session.run(
                """
                MATCH (source:Node {id: $source_id, user_id: $user_id})
                MATCH (target:Node {id: $target_id, user_id: $user_id})
                CREATE (source)-[r:RELATION {
                    id: $id,
                    relation_type: $relation_type,
                    direction: $direction,
                    intensity: $intensity,
                    confidence: $confidence,
                    context: $context,
                    status: $status,
                    created_at: datetime(),
                    updated_at: datetime()
                }]->(target)
                RETURN r
                """,
                source_id=data["source_id"],
                target_id=data["target_id"],
                id=relation_id,
                relation_type=data.get("relation_type", "affects"),
                direction=data.get("direction", "directed"),
                intensity=data.get("intensity", 1.0),
                confidence=data.get("confidence", 0.5),
                context=json.dumps(data.get("context", {})),
                status=data.get("status", "active")
            )
            
            record = await result.single()
            return self._record_to_dict(record["r"])
    
    async def propagate(self, source_id: str, depth: int = 3) -> List[Dict[str, Any]]:
        """Propaga impacto a partir de um nó"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH path = (start:Node {id: $id, user_id: $user_id})-[:RELATION*1..{depth}]-()
                RETURN path
                """,
                id=source_id,
                user_id=self.user_id,
                depth=depth
            )
            records = await result.fetch()
            return [self._record_to_dict(record) for record in records]
