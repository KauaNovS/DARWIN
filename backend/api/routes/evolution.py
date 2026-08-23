# api/routes/evolution.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.dependencies import get_current_user
from models.user import User
from services.evolution.sequence import SequenceManager

router = APIRouter()


class StartSequenceInput(BaseModel):
    path: str
    level: int = 1


@router.get("/current")
async def get_current_sequence(current_user: User = Depends(get_current_user)):
    manager = SequenceManager(str(current_user.id))
    return await manager.get_current_sequence()


@router.post("/start")
async def start_sequence(data: StartSequenceInput, current_user: User = Depends(get_current_user)):
    manager = SequenceManager(str(current_user.id))
    return await manager.start_sequence(data.path, data.level)
