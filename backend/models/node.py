# models/node.py - Grafo Relacional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
import uuid

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)  # person, emotion, habit, task, event, idea, etc.
    description = Column(String, nullable=True)
    context = Column(JSON, default={})
    intensity = Column(Float, default=1.0)  # 0-10
    weight = Column(Float, default=1.0)  # 1-10
    status = Column(String, default="active")
    # NOTE: renamed from `metadata` (original plan) — that name is reserved by
    # SQLAlchemy's Declarative API and breaks class creation.
    extra_metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
