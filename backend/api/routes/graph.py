# api/routes/graph.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from core.dependencies import get_current_user
from models.user import User
from services.graph.node_manager import NodeManager
from services.graph.relation_manager import RelationManager

router = APIRouter()


class NodeInput(BaseModel):
    name: str
    type: Optional[str] = "generic"
    description: Optional[str] = ""
    context: Dict[str, Any] = {}


class RelationInput(BaseModel):
    source_id: str
    target_id: str
    relation_type: Optional[str] = "affects"
    context: Dict[str, Any] = {}


@router.post("/nodes")
async def create_node(data: NodeInput, current_user: User = Depends(get_current_user)):
    manager = NodeManager(str(current_user.id))
    return await manager.create(data.model_dump())


@router.get("/nodes/{node_id}")
async def get_node(node_id: str, current_user: User = Depends(get_current_user)):
    manager = NodeManager(str(current_user.id))
    node = await manager.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Nó não encontrado")
    return node


@router.get("/nodes/{node_id}/relations")
async def get_node_relations(node_id: str, current_user: User = Depends(get_current_user)):
    manager = NodeManager(str(current_user.id))
    return await manager.get_relations(node_id)


@router.post("/relations")
async def create_relation(data: RelationInput, current_user: User = Depends(get_current_user)):
    manager = RelationManager(str(current_user.id))
    return await manager.create(data.model_dump())


@router.get("/relations/{source_id}/propagate")
async def propagate(source_id: str, depth: int = 3, current_user: User = Depends(get_current_user)):
    manager = RelationManager(str(current_user.id))
    return await manager.propagate(source_id, depth)
