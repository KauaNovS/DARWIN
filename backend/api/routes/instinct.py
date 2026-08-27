# api/routes/instinct.py
#
# NOVO: expõe a camada instintiva ("Darwin 2.0") que antes vivia isolada em
# app/ (scaffold desconectado, com imports quebrados) — agora integrada ao
# backend real, reaproveitando auth JWT (core.dependencies) e as conexões
# de banco já testadas (core.database).
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.dependencies import get_current_user
from models.user import User
from services.instinct.sentinel import OnboardingSentinel
from services.instinct.eco_listener import EcoListener
from services.instinct.halter_guardian import HalterGuardian
from services.instinct.genetic_memory import GeneticMemory
from services.instinct.wave_index import WaveIndex
from services.instinct.trust_boundary import TrustBoundary
from services.instinct.ai_service import AIEngine

router = APIRouter()


class UserState(BaseModel):
    sleep_quality: Optional[float] = 0.5
    anxiety: Optional[float] = 0.5
    workload: Optional[float] = 0.5
    behavior_event: Optional[str] = None  # typing, backspace, task_cancel, hesitation
    behavior_value: Optional[float] = 0.0
    performance_history: Optional[List[float]] = None


class AnswerRequest(BaseModel):
    question_index: int  # 0=energy, 1=focus, 2=conclusion
    answer: str


class FeedbackRequest(BaseModel):
    action_type: str
    approved: bool


# ---------------------------------------------------------------------------
# Onboarding (Fase Feto)
# ---------------------------------------------------------------------------

@router.get("/onboarding/questions")
async def get_onboarding_questions(current_user: User = Depends(get_current_user)):
    sentinel = OnboardingSentinel(str(current_user.id))
    return {
        "phase": await sentinel.get_phase(),
        "questions": sentinel.get_daily_questions(),
    }


@router.post("/onboarding/answer")
async def submit_onboarding_answer(
    req: AnswerRequest, current_user: User = Depends(get_current_user)
):
    if req.question_index < 0 or req.question_index >= len(OnboardingSentinel.QUESTION_KEYS):
        raise HTTPException(400, "Invalid question index")

    sentinel = OnboardingSentinel(str(current_user.id))
    question_key = OnboardingSentinel.QUESTION_KEYS[req.question_index]
    await sentinel.record_daily_answer(question_key, req.answer)
    advance = await sentinel.advance_phase()
    return {"status": "recorded", "phase_advance": advance}


@router.get("/onboarding/phase")
async def get_onboarding_phase(current_user: User = Depends(get_current_user)):
    sentinel = OnboardingSentinel(str(current_user.id))
    return {
        "phase": await sentinel.get_phase(),
        "active_days": await sentinel.get_days_active(),
    }


# ---------------------------------------------------------------------------
# Processo instintivo principal
# ---------------------------------------------------------------------------

@router.post("/process")
async def process_instinct(state: UserState, current_user: User = Depends(get_current_user)):
    """
    O "cérebro invisível" do Darwin: processa Onboarding, Eco, Halter,
    Wave Index, Genoma e Confiança de uma vez, e devolve um insight.
    """
    user_id = str(current_user.id)

    sentinel = OnboardingSentinel(user_id)
    phase = await sentinel.get_phase()
    phase_advance = await sentinel.advance_phase()

    eco = EcoListener(user_id)
    if state.behavior_event:
        await eco.feed_behavior(state.behavior_event, state.behavior_value or 0.0)
    inferred_context = await eco.infer_context()

    halter = HalterGuardian(user_id)
    halter_eval = await halter.evaluate({
        "sleep_quality": state.sleep_quality if state.sleep_quality is not None else inferred_context.get("inferred_energy", 0.5),
        "anxiety": state.anxiety if state.anxiety is not None else inferred_context.get("inferred_cognitive_load", 0.5),
        "workload": state.workload if state.workload is not None else 0.5,
    })
    can_create = await halter.can_create_task()

    trust = TrustBoundary(user_id)
    trust_decision = await trust.execute_or_ask({"type": "routine_adjustment"})

    wave = WaveIndex()
    performance = state.performance_history or [0.7, 0.75, 0.8, 0.72, 0.78, 0.82, 0.79]
    pressure = [0.3, 0.5, 0.7, 0.4, 0.6, 0.8, 0.5]
    mastery = wave.calculate_mastery(performance, pressure)

    genetic = GeneticMemory(user_id)
    genome = await genetic.get_genome()

    ai = AIEngine()
    insight = await ai.generate_insight({
        "phase": phase,
        "stress": halter_eval.get("stress_index", 0.5),
        "mastery": mastery["mastery_level"],
        "genome": genome.get("genome", []),
    })

    return {
        "phase": phase,
        "phase_advance": phase_advance,
        "inferred_context": inferred_context,
        "halter": halter_eval,
        "can_create_task": can_create,
        "trust": trust_decision,
        "mastery": mastery,
        "genome": genome,
        "insight": insight,
        "message": "Darwin processado com sucesso.",
    }


@router.post("/feedback")
async def record_feedback(req: FeedbackRequest, current_user: User = Depends(get_current_user)):
    """Registra feedback do usuário para ajustar a confiança (Trust Boundary)."""
    trust = TrustBoundary(str(current_user.id))
    new_confidence = await trust.record_feedback(req.action_type, req.approved)
    return {
        "action_type": req.action_type,
        "approved": req.approved,
        "new_confidence": new_confidence,
    }
