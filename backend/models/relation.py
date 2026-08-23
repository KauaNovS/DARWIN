# models/relation.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
import uuid

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    source_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))
    target_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))
    relation_type = Column(String)  # affects, improves, depends_on, belongs_to, etc.
    direction = Column(String, default="directed")  # directed, bidirectional
    intensity = Column(Float, default=1.0)  # 1-10
    confidence = Column(Float, default=0.5)  # 0-1
    context = Column(JSON, default={})
    status = Column(String, default="active")
    # NOTE: renamed from `metadata` (original plan) — that name is reserved by
    # SQLAlchemy's Declarative API and breaks class creation.
    extra_metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
