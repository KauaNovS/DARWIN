from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import get_current_user
from services.sequences.paths import PATHS, get_sequence_for_beyonder, get_next_level_requirements
from models.beyonder import User

router = APIRouter()

@router.get("/paths")
async def list_paths():
    return [
        {
            "key": k,
            "name": v["name"],
            "archetype": v["archetype"],
            "description": v["description"],
            "levels_count": len(v["levels"]),
        }
        for k, v in PATHS.items()
    ]

@router.get("/paths/{path_key}")
async def get_path(path_key: str):
    path = PATHS.get(path_key.upper())
    if not path:
        raise HTTPException(status_code=404, detail="Caminho nao encontrado")
    return path

@router.get("/my-sequence")
async def get_my_sequence(current_user: User = Depends(get_current_user)):
    beyonder = current_user.beyonder
    if not beyonder:
        raise HTTPException(status_code=404, detail="Perfil Beyonder nao encontrado. Complete o onboarding.")
    seq = get_sequence_for_beyonder(beyonder.path, beyonder.sequence_level)
    next_req = get_next_level_requirements(beyonder.path, beyonder.sequence_level)
    return {
        "path": beyonder.path,
        "path_name": PATHS.get(beyonder.path, {}).get("name", ""),
        "level": beyonder.sequence_level,
        "title": beyonder.sequence_title,
        "current_sequence": seq,
        "next_requirements": next_req,
        "digestion_score": beyonder.digestion_score,
        "total_xp": beyonder.total_xp,
        "potion_stability": beyonder.potion_stability,
        "shadow_index": beyonder.shadow_index,
    }
