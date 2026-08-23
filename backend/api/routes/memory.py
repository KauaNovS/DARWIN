# api/routes/memory.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from core.dependencies import get_current_user
from models.user import User
from services.memory.live_memory import LiveMemory

router = APIRouter()


class StoreInput(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = "memory"
    context: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    related_memories: List[str] = []


@router.post("/")
async def store_memory(data: StoreInput, current_user: User = Depends(get_current_user)):
    memory = LiveMemory(str(current_user.id))
    return await memory.store(data.model_dump())


@router.get("/search")
async def search_memory(type: Optional[str] = None, current_user: User = Depends(get_current_user)):
    memory = LiveMemory(str(current_user.id))
    query: Dict[str, Any] = {}
    if type:
        query["type"] = type
    return await memory.search(query)
