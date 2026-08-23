import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta

class WaveIndex:
    """
    A Matemática da Digestão.
    Domínio real = Baixa variância em contextos de alta pressão.
    """
    
    def __init__(self):
        self.window_days = 14

    def calculate_mastery(self, performance_history: List[float], pressure_contexts: List[float]) -> Dict[str, Any]:
        """
        performance_history: scores de 0 a 1 (ex: conclusão de tarefas, qualidade de sono)
        pressure_contexts: scores de pressão (0 = calmo, 1 = crise extrema)
        """
        if len(performance_history) < 7:
            return {"mastery_level": 0.0, "status": "insufficient_data"}
        
        # 1. Variância Base
        variance = np.var(performance_history)
        
        # 2. Desempenho sob Pressão (pegamos os 20% momentos de maior pressão)
        sorted_pairs = sorted(zip(pressure_contexts, performance_history), reverse=True)
        high_pressure_count = max(1, int(len(sorted_pairs) * 0.2))
        high_pressure_performances = [p for _, p in sorted_pairs[:high_pressure_count]]
        
        pressure_variance = np.var(high_pressure_performances) if high_pressure_performances else 1.0
        pressure_mean = np.mean(high_pressure_performances) if high_pressure_performances else 0.0
        
        # 3. Fórmula do Domínio
        # Quanto menor a variância total e a variância sob pressão, maior o domínio.
        # Quanto maior a média sob pressão, maior o domínio.
        normalized_variance = 1 / (1 + variance * 5)  # Quanto menor variance, mais perto de 1
        normalized_pressure_variance = 1 / (1 + pressure_variance * 5)
        
        mastery_score = (normalized_variance * 0.4) + (normalized_pressure_variance * 0.4) + (pressure_mean * 0.2)
        
        # Threshold para liberar próxima Sequência (exige 0.85)
        return {
            "mastery_level": round(min(mastery_score, 1.0), 3),
            "variance": round(variance, 3),
            "pressure_performance_mean": round(pressure_mean, 3),
            "ready_to_advance": mastery_score >= 0.85,
            "advance_confidence": "ALTA" if mastery_score >= 0.85 else "MEDIA" if mastery_score >= 0.6 else "BAIXA"
        }
