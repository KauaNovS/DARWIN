# services/memory/live_memory.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from services.graph.node_manager import NodeManager
from services.graph.relation_manager import RelationManager

class LiveMemory:
    """Memória Viva do Darwin"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.node_manager = NodeManager(user_id)
        self.relation_manager = RelationManager(user_id)
    
    async def store(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Armazena uma memória com contexto"""
        # Cria nó principal
        node = await self.node_manager.create({
            "name": data.get("name", "Untitled Memory"),
            "type": data.get("type", "memory"),
            "context": data.get("context", {}),
            "metadata": data.get("metadata", {})
        })
        
        # Conecta a memórias relacionadas
        if data.get("related_memories"):
            for related_id in data["related_memories"]:
                await self.relation_manager.create({
                    "source_id": node["id"],
                    "target_id": related_id,
                    "relation_type": "related_to",
                    "context": data.get("context", {})
                })
        
        # Extrai padrões
        patterns = await self._extract_patterns(data)
        
        return {
            "node": node,
            "patterns": patterns
        }
    
    async def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca memórias por critérios (chamado por services/evolution/sequence.py
        mas nunca definido no plano original — delega para o node_manager)."""
        return await self.node_manager.search(query)

    async def retrieve(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera memórias relevantes"""
        # Busca semântica (implementar com embeddings)
        # Busca contextual
        # Busca relacional
        pass
    
    async def get_relevant_context(self, input_text: str) -> Dict[str, Any]:
        """Obtém contexto relevante para uma entrada"""
        # 1. Busca memórias recentes
        recent = await self.get_recent(limit=10)
        
        # 2. Busca memórias relacionadas semanticamente
        semantic = await self.retrieve(input_text, limit=5)
        
        # 3. Busca padrões ativos
        patterns = await self._get_active_patterns()
        
        return {
            "recent": recent,
            "semantic": semantic,
            "patterns": patterns,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _extract_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrai padrões de uma nova memória"""
        # TODO: Implementar extração de padrões
        pass
    
    async def _get_active_patterns(self) -> List[Dict[str, Any]]:
        """Obtém padrões ativos do usuário"""
        # TODO: Implementar
        pass
