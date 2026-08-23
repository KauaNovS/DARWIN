# api/routes/health.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Verifica se a API está no ar."""
    return {"status": "ok"}
