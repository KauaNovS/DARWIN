# services/ia/patterns.py
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import numpy as np
from services.memory.live_memory import LiveMemory
from services.graph.propagation import PropagationAnalyzer

class PatternDetector:
    """Detecta padrões no comportamento do usuário"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = LiveMemory(user_id)
        self.propagation = PropagationAnalyzer(user_id)
    
    async def detect_patterns(self, timeframe: int = 30) -> List[Dict[str, Any]]:
        """Detecta padrões em um período"""
        patterns = []
        
        # Padrões emocionais
        emotional = await self._detect_emotional_patterns(timeframe)
        patterns.extend(emotional)
        
        # Padrões energéticos
        energy = await self._detect_energy_patterns(timeframe)
        patterns.extend(energy)
        
        # Padrões operacionais
        operational = await self._detect_operational_patterns(timeframe)
        patterns.extend(operational)
        
        # Padrões relacionais
        relational = await self._detect_relational_patterns(timeframe)
        patterns.extend(relational)
        
        # Padrões de corrupção
        corruption = await self._detect_corruption_patterns(timeframe)
        patterns.extend(corruption)
        
        return patterns
    
    async def _detect_emotional_patterns(self, timeframe: int) -> List[Dict[str, Any]]:
        """Detecta padrões emocionais"""
        # Busca registros emocionais
        emotions = await self.memory.search({
            "type": "emotion",
            "timeframe": timeframe
        })
        
        patterns = []
        
        if len(emotions) > 5:
            # Analisa recorrência de emoções
            emotion_counts = {}
            for e in emotions:
                emotion = e.get("context", {}).get("emotion")
                if emotion:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            for emotion, count in emotion_counts.items():
                if count > len(emotions) * 0.3:  # Mais de 30% das ocorrências
                    patterns.append({
                        "type": "emotional",
                        "subtype": "recurrent_emotion",
                        "emotion": emotion,
                        "frequency": count / len(emotions),
                        "confidence": min(count / 10, 0.9)
                    })
            
            # Detecta gatilhos emocionais
            triggers = await self._detect_emotional_triggers(emotions)
            patterns.extend(triggers)
        
        return patterns
    
    async def _detect_energy_patterns(self, timeframe: int) -> List[Dict[str, Any]]:
        """Detecta padrões energéticos"""
        # Busca registros de energia
        energy_logs = await self.memory.search({
            "type": "energy",
            "timeframe": timeframe
        })
        
        patterns = []
        
        if len(energy_logs) > 5:
            # Calcula tendência
            values = [e.get("context", {}).get("value", 5) for e in energy_logs]
            trend = np.polyfit(range(len(values)), values, 1)[0]
            
            if abs(trend) > 0.05:
                patterns.append({
                    "type": "energy",
                    "subtype": "trend",
                    "direction": "increasing" if trend > 0 else "decreasing",
                    "rate": abs(trend),
                    "confidence": min(abs(trend) * 2, 0.9)
                })
            
            # Detecta ciclos
            cycles = await self._detect_cycles(values)
            if cycles:
                patterns.append({
                    "type": "energy",
                    "subtype": "cycle",
                    "period": cycles.get("period", 7),
                    "amplitude": cycles.get("amplitude", 1),
                    "confidence": cycles.get("confidence", 0.5)
                })
        
        return patterns
    
    async def _detect_operational_patterns(self, timeframe: int) -> List[Dict[str, Any]]:
        """Detecta padrões operacionais"""
        # Busca registros de tarefas
        tasks = await self.memory.search({
            "type": "task",
            "timeframe": timeframe
        })
        
        patterns = []
        
        if len(tasks) > 10:
            # Taxa de conclusão
            completed = [t for t in tasks if t.get("status") == "completed"]
            completion_rate = len(completed) / len(tasks)
            
            patterns.append({
                "type": "operational",
                "subtype": "completion_rate",
                "value": completion_rate,
                "confidence": min(len(tasks) / 20, 0.9)
            })
            
            # Horários de maior produtividade
            peak_times = await self._detect_peak_times(tasks)
            if peak_times:
                patterns.append({
                    "type": "operational",
                    "subtype": "peak_times",
                    "times": peak_times,
                    "confidence": 0.7
                })
        
        return patterns
    
    async def _detect_relational_patterns(self, timeframe: int) -> List[Dict[str, Any]]:
        """Detecta padrões relacionais"""
        # Busca registros de interações
        interactions = await self.memory.search({
            "type": "interaction",
            "timeframe": timeframe
        })
        
        patterns = []
        
        if len(interactions) > 5:
            # Impacto emocional de pessoas
            person_impact = {}
            for i in interactions:
                person = i.get("context", {}).get("person")
                emotion = i.get("context", {}).get("emotion_impact", 0)
                if person:
                    person_impact[person] = person_impact.get(person, 0) + emotion
            
            for person, impact in person_impact.items():
                if abs(impact) > 5:
                    patterns.append({
                        "type": "relational",
                        "subtype": "person_impact",
                        "person": person,
                        "impact": impact,
                        "confidence": min(abs(impact) / 10, 0.8)
                    })
        
        return patterns
    
    async def _detect_corruption_patterns(self, timeframe: int) -> List[Dict[str, Any]]:
        """Detecta padrões de corrupção"""
        patterns = []
        
        # Verifica indicadores de burnout
        burnout = await self._detect_burnout_risk(timeframe)
        if burnout:
            patterns.append(burnout)
        
        # Verifica loops destrutivos
        loops = await self._detect_destructive_loops(timeframe)
        patterns.extend(loops)
        
        return patterns
    
    async def _detect_burnout_risk(self, timeframe: int) -> Optional[Dict[str, Any]]:
        """Detecta risco de burnout"""
        # Coleta indicadores
        energy_decline = await self._get_energy_decline(timeframe)
        sleep_quality = await self._get_sleep_quality(timeframe)
        stress_level = await self._get_stress_level(timeframe)
        
        risk_score = 0
        risk_score += energy_decline * 0.4
        risk_score += (1 - sleep_quality) * 0.3
        risk_score += stress_level * 0.3
        
        if risk_score > 0.7:
            return {
                "type": "corruption",
                "subtype": "burnout_risk",
                "risk_score": risk_score,
                "indicators": {
                    "energy_decline": energy_decline,
                    "sleep_quality": sleep_quality,
                    "stress_level": stress_level
                },
                "recommendation": "Reduzir carga operacional e priorizar recuperação"
            }
        
        return None
