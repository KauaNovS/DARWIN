# services/ia/recommendation.py
from typing import Dict, Any, List, Optional
from services.ia.patterns import PatternDetector
from services.memory.live_memory import LiveMemory
from services.evolution.sequence import SequenceManager

class RecommendationEngine:
    """Motor de recomendações do Darwin"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pattern_detector = PatternDetector(user_id)
        self.memory = LiveMemory(user_id)
        self.sequence_manager = SequenceManager(user_id)
    
    async def generate_recommendations(self) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas no estado atual"""
        recommendations = []
        
        # Detecta padrões
        patterns = await self.pattern_detector.detect_patterns()
        
        # Recomendações baseadas em padrões
        for pattern in patterns:
            rec = await self._recommend_from_pattern(pattern)
            if rec:
                recommendations.append(rec)
        
        # Recomendações baseadas em sequência
        sequence_recs = await self._recommend_from_sequence()
        recommendations.extend(sequence_recs)
        
        # Recomendações baseadas em contexto
        context_recs = await self._recommend_from_context()
        recommendations.extend(context_recs)
        
        # Ordena por prioridade
        recommendations.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return recommendations
    
    async def _recommend_from_pattern(self, pattern: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Gera recomendação baseada em um padrão"""
        if pattern["type"] == "emotional" and pattern["subtype"] == "recurrent_emotion":
            if pattern["emotion"] in ["anxiety", "stress", "frustration"]:
                return {
                    "type": "action",
                    "category": "emotional_regulation",
                    "title": "Gerenciar " + pattern["emotion"],
                    "description": f"Você tem registrado {pattern['emotion']} com frequência. Considere:",
                    "actions": [
                        "Registrar o que está causando essa emoção",
                        "Praticar respiração profunda",
                        "Conversar com alguém de confiança"
                    ],
                    "priority": 4,
                    "confidence": pattern.get("confidence", 0.5)
                }
        
        elif pattern["type"] == "energy" and pattern["subtype"] == "trend":
            if pattern["direction"] == "decreasing":
                return {
                    "type": "action",
                    "category": "energy_recovery",
                    "title": "Recuperar energia",
                    "description": f"Sua energia está diminuindo (taxa: {pattern['rate']:.2f}). Recomendo:",
                    "actions": [
                        "Aumentar horas de sono",
                        "Fazer pausas regulares",
                        "Revisar alimentação"
                    ],
                    "priority": 3,
                    "confidence": pattern.get("confidence", 0.5)
                }
        
        elif pattern["type"] == "operational" and pattern["subtype"] == "completion_rate":
            if pattern["value"] < 0.6:
                return {
                    "type": "action",
                    "category": "productivity",
                    "title": "Melhorar taxa de conclusão",
                    "description": f"Sua taxa de conclusão está em {pattern['value']*100:.0f}%. Considere:",
                    "actions": [
                        "Reduzir número de tarefas simultâneas",
                        "Priorizar tarefas mais importantes",
                        "Dividir tarefas grandes em partes menores"
                    ],
                    "priority": 4,
                    "confidence": pattern.get("confidence", 0.5)
                }
        
        elif pattern["type"] == "corruption" and pattern["subtype"] == "burnout_risk":
            return {
                "type": "urgent",
                "category": "recovery",
                "title": "⚠️ Risco de Burnout Detectado",
                "description": f"Seu nível de risco é {pattern['risk_score']*100:.0f}%. Ação urgente:",
                "actions": [
                    "Reduzir carga de trabalho imediatamente",
                    "Priorizar sono e recuperação",
                    "Considerar pausa em projetos exigentes"
                ],
                "priority": 5,
                "confidence": pattern.get("confidence", 0.8)
            }
        
        return None
    
    async def _recommend_from_sequence(self) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas na sequência atual"""
        sequence = await self.sequence_manager.get_current_sequence()
        recommendations = []
        
        if sequence:
            # Verifica progresso
            if sequence["progress"] < 30:
                recommendations.append({
                    "type": "action",
                    "category": "evolution",
                    "title": f"Começar a Sequência {sequence['level']}",
                    "description": f"Você está no início da sequência. Comece pelos fundamentos.",
                    "actions": sequence.get("start_actions", []),
                    "priority": 3,
                    "confidence": 0.8
                })
            elif sequence["progress"] < 70:
                recommendations.append({
                    "type": "action",
                    "category": "evolution",
                    "title": f"Progresso da Sequência {sequence['level']}",
                    "description": f"Você está em {sequence['progress']:.0f}% da sequência. Continue!",
                    "actions": sequence.get("continue_actions", []),
                    "priority": 2,
                    "confidence": 0.8
                })
            else:
                recommendations.append({
                    "type": "action",
                    "category": "evolution",
                    "title": "Pronto para próxima fase",
                    "description": f"Você está próximo de completar a sequência!",
                    "actions": sequence.get("completion_actions", []),
                    "priority": 3,
                    "confidence": 0.8
                })
        
        return recommendations
    
    async def _recommend_from_context(self) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas no contexto atual"""
        # TODO: Implementar recomendações contextuais
        return []
