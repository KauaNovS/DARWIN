# api/routes/users.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter, Depends

from core.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna o perfil do usuário logado."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "meta_final": current_user.meta_final,
        "identity": current_user.identity,
        "preferences": current_user.preferences,
    }
