# services/instinct/wave_index.py
#
# "Matemática da Digestão": domínio real = baixa variância em contextos de
# alta pressão, não uma nota autoatribuída. Sem dependências externas de
# banco — puro cálculo, por isso não precisou de correção estrutural.
import numpy as np
from typing import List, Dict, Any


class WaveIndex:
    def __init__(self):
        self.window_days = 14

    def calculate_mastery(
        self,
        performance_history: List[float],
        pressure_contexts: List[float],
    ) -> Dict[str, Any]:
        """
        performance_history: scores 0-1 (conclusão de tarefas, qualidade de sono, etc.)
        pressure_contexts: scores 0-1 (0 = calmo, 1 = crise extrema)
        """
        if len(performance_history) < 7:
            return {
                "mastery_level": 0.0,
                "status": "insufficient_data",
                "ready_to_advance": False,
            }

        variance = float(np.var(performance_history))

        sorted_pairs = sorted(zip(pressure_contexts, performance_history), reverse=True)
        high_pressure_count = max(1, int(len(sorted_pairs) * 0.2))
        high_pressure_performances = [p for _, p in sorted_pairs[:high_pressure_count]]

        pressure_variance = float(np.var(high_pressure_performances)) if high_pressure_performances else 1.0
        pressure_mean = float(np.mean(high_pressure_performances)) if high_pressure_performances else 0.0

        normalized_variance = 1 / (1 + variance * 5)
        normalized_pressure_variance = 1 / (1 + pressure_variance * 5)

        mastery_score = (
            (normalized_variance * 0.4)
            + (normalized_pressure_variance * 0.4)
            + (pressure_mean * 0.2)
        )
        mastery_score = round(min(mastery_score, 1.0), 3)

        return {
            "mastery_level": mastery_score,
            "variance": round(variance, 3),
            "pressure_performance_mean": round(pressure_mean, 3),
            "ready_to_advance": mastery_score >= 0.85,
            "status": "mature" if mastery_score >= 0.7 else "developing",
            "advance_confidence": (
                "ALTA" if mastery_score >= 0.85 else "MEDIA" if mastery_score >= 0.6 else "BAIXA"
            ),
        }
