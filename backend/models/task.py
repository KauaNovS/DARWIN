# models/task.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=3)  # 1-5
    difficulty = Column(Integer, default=3)  # 1-10
    status = Column(String, default="pending")  # pending, in_progress, done, abandoned
    context = Column(JSON, default={})  # Contexto da tarefa
    xp = Column(Integer, default=0)
    sequence_id = Column(UUID(as_uuid=True), ForeignKey("sequences.id"), nullable=True)
    potion_id = Column(UUID(as_uuid=True), ForeignKey("potions.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
