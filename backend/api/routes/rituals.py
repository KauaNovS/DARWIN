from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.dependencies import get_current_user, get_db
from models.beyonder import User, Beyonder, Ritual
from services.potions.engine import (
    calculate_potion_score, calculate_digestion_delta,
    calculate_xp_for_ritual, check_level_advancement, analyze_shadow
)
from pydantic import BaseModel
from typing import Optional
from datetime import date

router = APIRouter()

class RitualIn(BaseModel):
    date: str                           # YYYY-MM-DD
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    water_ml: Optional[int] = None
    nutrition_score: Optional[int] = None
    movement_minutes: Optional[int] = None
    movement_type: Optional[str] = None
    reading_minutes: Optional[int] = None
    meditation_minutes: Optional[int] = None
    journaling: Optional[bool] = False
    emotional_state: Optional[int] = None
    anxiety_level: Optional[int] = None
    social_connection: Optional[int] = None
    notes: Optional[str] = None
    insights: Optional[str] = None
    gratitude: Optional[str] = None

@router.post("/")
async def register_ritual(
    data: RitualIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    beyonder = current_user.beyonder
    if not beyonder:
        raise HTTPException(status_code=404, detail="Perfil Beyonder nao encontrado")

    # Criar ritual
    ritual = Ritual(
        beyonder_id=beyonder.id,
        **data.dict()
    )

    # Calcular score
    potion_score = calculate_potion_score(ritual)
    ritual.potion_score = potion_score

    # Calcular variacao na digestao
    delta = calculate_digestion_delta(potion_score, beyonder.digestion_score)
    ritual.digestion_delta = delta

    # XP ganho
    xp = calculate_xp_for_ritual(ritual, potion_score)

    # Atualizar Beyonder
    beyonder.digestion_score = max(0.0, min(100.0, beyonder.digestion_score + delta))
    beyonder.total_xp += xp

    # Verificar se pode subir de nivel
    advancement = check_level_advancement(beyonder)

    # Analisar sombra (ultimos 30 rituals)
    result = await db.execute(
        select(Ritual).where(Ritual.beyonder_id == beyonder.id)
        .order_by(Ritual.created_at.desc()).limit(30)
    )
    recent_rituals = result.scalars().all()
    shadow = analyze_shadow(recent_rituals + [ritual])
    beyonder.shadow_index = shadow["shadow_index"]

    db.add(ritual)
    db.add(beyonder)
    await db.commit()
    await db.refresh(ritual)

    return {
        "ritual_id": ritual.id,
        "potion_score": potion_score,
        "digestion_delta": delta,
        "new_digestion": beyonder.digestion_score,
        "xp_gained": xp,
        "total_xp": beyonder.total_xp,
        "shadow_analysis": shadow,
        "can_advance": advancement["can_advance"],
        "advancement_info": advancement,
        "message": _potion_message(potion_score),
    }

def _potion_message(score: float) -> str:
    if score >= 90:
        return "A pocao foi absorvida perfeitamente. O caminho se ilumina."
    elif score >= 70:
        return "Boa digestao. Continue. A nevoa comeca a se dissipar."
    elif score >= 50:
        return "Digestao parcial. Ha resistencia -- observe o que falta."
    elif score >= 30:
        return "A pocao mal foi tocada. O Beyonder hesita."
    else:
        return "A pocao foi rejeitada. O sistema requer atencao urgente."

@router.get("/")
async def list_rituals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    beyonder = current_user.beyonder
    if not beyonder:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")
    result = await db.execute(
        select(Ritual).where(Ritual.beyonder_id == beyonder.id)
        .order_by(Ritual.created_at.desc()).limit(90)
    )
    rituals = result.scalars().all()
    return rituals

@router.get("/today")
async def get_today_ritual(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    beyonder = current_user.beyonder
    if not beyonder:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")
    today = date.today().isoformat()
    result = await db.execute(
        select(Ritual).where(
            Ritual.beyonder_id == beyonder.id,
            Ritual.date == today
        )
    )
    ritual = result.scalar_one_or_none()
    return ritual or {"message": "Nenhum ritual registrado hoje.", "date": today}
