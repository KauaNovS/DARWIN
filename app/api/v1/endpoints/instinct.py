from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.sentinel import OnboardingSentinel
from app.services.eco_listener import EcoListener
from app.services.halter_guardian import HalterGuardian
from app.services.genetic_memory import GeneticMemory
from app.core.wave_index import WaveIndex
from app.core.trust_boundary import TrustBoundary
from app.api.v1.dependencies import get_current_user

router = APIRouter()

class UserState(BaseModel):
    sleep_quality: Optional[float] = 0.5
    anxiety: Optional[float] = 0.5
    workload: Optional[float] = 0.5
    behavior_event: Optional[str] = None  # typing, task_cancel
    behavior_value: Optional[float] = 0.0

@router.post("/instinct/process")
async def process_instinct(state: UserState, current_user = Depends(get_current_user)):
    """O cérebro invisível do Darwin. Processa tudo de uma vez."""
    user_id = current_user.id
    
    # 1. Onboarding
    sentinel = OnboardingSentinel(user_id)
    phase = await sentinel.get_phase()
    
    # 2. Eco - Escuta Implícita
    eco = EcoListener(user_id)
    if state.behavior_event:
        await eco.feed_behavior(state.behavior_event, state.behavior_value)
    inferred_context = await eco.infer_context()
    
    # 3. Halter - Anjo da Guarda (Sempre avalia)
    halter = HalterGuardian(user_id)
    halter_eval = await halter.evaluate({
        "sleep_quality": state.sleep_quality or inferred_context.get("inferred_energy", 0.5),
        "anxiety": state.anxiety,
        "workload": state.workload
    })
    
    # 4. Trust Boundary - Decisão de Autonomia
    trust = TrustBoundary(user_id)
    trust_decision = await trust.execute_or_ask({"type": "routine_adjustment"})
    
    # 5. Wave Index - Matemática da Digestão
    wave = WaveIndex()
    # Mock: performance_history viria do banco
    mastery = wave.calculate_mastery([0.8, 0.85, 0.9, 0.88, 0.92], [0.5, 0.3, 0.8, 0.2, 0.9])
    
    # 6. Genetic Memory - Compressão (Executa a cada 24h, mas chamamos aqui para testar)
    genetic = GeneticMemory(user_id)
    genome = await genetic.distill()
    
    return {
        "phase": phase,
        "inferred_context": inferred_context,
        "halter": halter_eval,
        "trust": trust_decision,
        "mastery": mastery,
        "genome": genome,
        "message": "Darwin processado com sucesso. Evolução invisível em ação."
    }
