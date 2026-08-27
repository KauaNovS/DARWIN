# models/stress.py
#
# Não é uma tabela SQL: o índice de estresse é calculado sob demanda e
# cacheado no Redis pelo HalterGuardian.
from pydantic import BaseModel


class StressIndex(BaseModel):
    user_id: str
    sleep_score: float  # 0-1
    anxiety_score: float  # 0-1
    workload_score: float  # 0-1
    stress_level: float  # 0-1
    timestamp: str
    halter_activated: bool = False
    recovery_mode: bool = False
