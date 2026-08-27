from fastapi import APIRouter, Depends
from core.dependencies import get_current_user
from models.beyonder import User
from services.sequences.paths import PATHS, get_sequence_for_beyonder

router = APIRouter()

@router.get("/current")
async def get_current_potion(current_user: User = Depends(get_current_user)):
    beyonder = current_user.beyonder
    if not beyonder:
        return {"message": "Complete o onboarding para receber sua primeira pocao."}
    seq = get_sequence_for_beyonder(beyonder.path, beyonder.sequence_level)
    path_data = PATHS.get(beyonder.path, {})
    return {
        "path": beyonder.path,
        "path_name": path_data.get("name", ""),
        "level": beyonder.sequence_level,
        "sequence_title": beyonder.sequence_title,
        "potion_name": seq.get("potion", ""),
        "ingredients": seq.get("ingredients", []),
        "digestion_score": beyonder.digestion_score,
        "digestion_threshold": seq.get("digestion_threshold", 100),
        "stability": beyonder.potion_stability,
        "progress_pct": round(
            min(beyonder.digestion_score / max(seq.get("digestion_threshold", 1), 1) * 100, 100), 1
        ),
    }

@router.get("/all-potions/{path_key}")
async def list_all_potions(path_key: str):
    path = PATHS.get(path_key.upper())
    if not path:
        return {"error": "Caminho nao encontrado"}
    return [
        {
            "level": lvl["level"],
            "title": lvl["title"],
            "potion": lvl["potion"],
            "ingredients": lvl["ingredients"],
            "description": lvl["description"],
        }
        for lvl in path["levels"]
    ]
