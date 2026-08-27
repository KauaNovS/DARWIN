from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.dependencies import get_current_user, get_db
from models.beyonder import User, Ritual, Memory
from datetime import date, timedelta

router = APIRouter()

@router.get("/summary")
async def get_memory_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    beyonder = current_user.beyonder
    if not beyonder:
        return {"message": "Perfil nao encontrado"}

    # Ultimos 30 dias
    since = (date.today() - timedelta(days=30)).isoformat()
    result = await db.execute(
        select(Ritual).where(
            Ritual.beyonder_id == beyonder.id,
            Ritual.date >= since
        ).order_by(Ritual.date.asc())
    )
    rituals = result.scalars().all()

    if not rituals:
        return {"message": "Nenhum ritual nos ultimos 30 dias."}

    # Calcular medias
    avg_sleep = sum(r.sleep_hours or 0 for r in rituals) / len(rituals)
    avg_potion = sum(r.potion_score or 0 for r in rituals) / len(rituals)
    avg_emotion = sum(r.emotional_state or 5 for r in rituals) / len(rituals)
    journaling_rate = sum(1 for r in rituals if r.journaling) / len(rituals)

    return {
        "period": "30 dias",
        "rituals_count": len(rituals),
        "avg_potion_score": round(avg_potion, 1),
        "avg_sleep_hours": round(avg_sleep, 1),
        "avg_emotional_state": round(avg_emotion, 1),
        "journaling_rate": round(journaling_rate * 100, 1),
        "current_digestion": beyonder.digestion_score,
        "shadow_index": beyonder.shadow_index,
        "total_xp": beyonder.total_xp,
    }
