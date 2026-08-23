# api/routes/tasks.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
# CRUD mínimo em cima do modelo Task já existente.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import uuid

from core.database import get_db
from core.dependencies import get_current_user
from models.user import User
from models.task import Task

router = APIRouter()


class TaskInput(BaseModel):
    title: str
    description: Optional[str] = None


@router.get("/")
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    return result.scalars().all()


@router.post("/")
async def create_task(
    data: TaskInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(user_id=current_user.id, title=data.title, description=data.description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    await db.delete(task)
    await db.commit()
    return {"deleted": True}
