# services/evolution/sequence.py
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
from services.memory.live_memory import LiveMemory

class SequenceManager:
    """Gerencia sequências evolutivas"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = LiveMemory(user_id)
    
    async def get_current_sequence(self) -> Optional[Dict[str, Any]]:
        """Obtém a sequência atual do usuário"""
        # Busca sequência ativa
        sequences = await self.memory.search({
            "type": "sequence",
            "status": "active"
        })
        
        if sequences:
            return sequences[0]
        return None
    
    async def start_sequence(self, path: str, level: int) -> Dict[str, Any]:
        """Inicia uma nova sequência"""
        sequence_data = {
            "name": f"{path}_level_{level}",
            "path": path,
            "level": level,
            "status": "discovery",
            "progress": 0.0,
            "started_at": datetime.utcnow().isoformat()
        }
        
        # Cria a sequência na memória
        sequence = await self.memory.store({
            "type": "sequence",
            "data": sequence_data,
            "context": {
                "path": path,
                "level": level
            }
        })
        
        # Cria a Poção correspondente
        # NOTE: memory.store() retorna {"node": ..., "patterns": ...}, não um dict
        # com "id" no topo — corrigido aqui (bug do plano original).
        await self._create_potion(sequence["node"]["id"], path, level)

        return sequence
    
    async def _create_potion(self, sequence_id: str, path: str, level: int) -> Dict[str, Any]:
        """Cria a poção correspondente à sequência"""
        potion_data = {
            "name": f"Poção do {path} - Nível {level}",
            "sequence_id": sequence_id,
            "ingredients": self._get_ingredients(path, level),
            "status": "brewing"
        }
        
        return await self.memory.store({
            "type": "potion",
            "data": potion_data,
            "context": {
                "sequence_id": sequence_id,
                "path": path,
                "level": level
            }
        })
    
    def _get_ingredients(self, path: str, level: int) -> List[str]:
        """Obtém ingredientes para uma poção"""
        # TODO: Implementar lógica de ingredientes baseada no caminho e nível
        base_ingredients = [
            "registro_diario",
            "consistencia",
            "reflexao",
            "aplicacao_pratica"
        ]
        
        if level <= 5:
            base_ingredients.extend([
                "dominio_teorico",
                "pratica_controlada",
                "feedback_externo"
            ])
        
        if level <= 3:
            base_ingredients.extend([
                "integracao_sistemica",
                "expansao_operacional",
                "arquitetura_pessoal"
            ])
        
        return base_ingredients
