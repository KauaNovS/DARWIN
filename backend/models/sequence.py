# models/sequence.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
import uuid


class Sequence(Base):
    __tablename__ = "sequences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    path = Column(String)  # Caminho ao qual pertence
    level = Column(Integer)  # 9 a 0 (quanto menor, mais avançado)
    description = Column(String)
    potion_id = Column(UUID(as_uuid=True), ForeignKey("potions.id"))
    status = Column(String, default="discovery")  # discovery, understanding, application, consistency, control, mastery, integration, expansion, architecture, operational_ascent
    progress = Column(Float, default=0.0)  # 0-100
    context = Column(JSON, default={})
    started_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
