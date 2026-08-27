from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from core.database import Base

def new_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id               = Column(String, primary_key=True, default=new_id)
    email            = Column(String, unique=True, nullable=False)
    name             = Column(String, nullable=False)
    hashed_password  = Column(String, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)
    beyonder         = relationship("Beyonder", back_populates="user", uselist=False)

class Beyonder(Base):
    # Perfil evolutivo do usuario
    __tablename__ = "beyonders"
    id               = Column(String, primary_key=True, default=new_id)
    user_id          = Column(String, ForeignKey("users.id"), unique=True)
    # Caminho: FOOL | OBSERVER | ALCHEMIST | GUARDIAN | ARCHITECT
    path             = Column(String, nullable=False, default="FOOL")
    sequence_level   = Column(Integer, nullable=False, default=9)
    sequence_title   = Column(String, nullable=False, default="Estudante do Caos")
    total_xp         = Column(Float, nullable=False, default=0.0)
    digestion_score  = Column(Float, nullable=False, default=0.0)   # 0-100
    potion_stability = Column(Float, nullable=False, default=0.0)   # consistencia
    shadow_index     = Column(Float, nullable=False, default=0.0)   # sombra psicologica
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user             = relationship("User", back_populates="beyonder")
    rituals          = relationship("Ritual", back_populates="beyonder")
    potion_logs      = relationship("PotionLog", back_populates="beyonder")
    memories         = relationship("Memory", back_populates="beyonder")

class Ritual(Base):
    # Registro diario -- ingredientes da pocao
    __tablename__ = "rituals"
    id               = Column(String, primary_key=True, default=new_id)
    beyonder_id      = Column(String, ForeignKey("beyonders.id"))
    date             = Column(String, nullable=False)               # YYYY-MM-DD

    # Ingredientes fisicos
    sleep_hours      = Column(Float)
    sleep_quality    = Column(Integer)                              # 1-10
    water_ml         = Column(Integer)
    nutrition_score  = Column(Integer)                              # 1-10
    movement_minutes = Column(Integer)
    movement_type    = Column(String)                               # strength|cardio|yoga|walk

    # Ingredientes cognitivos
    reading_minutes  = Column(Integer)
    meditation_minutes = Column(Integer)
    journaling       = Column(Boolean, default=False)

    # Ingredientes emocionais
    emotional_state  = Column(Integer)                              # 1-10
    anxiety_level    = Column(Integer)                              # 1-10
    social_connection = Column(Integer)                             # 1-10

    # Anotacoes livres
    notes            = Column(Text)
    insights         = Column(Text)
    gratitude        = Column(Text)

    # Score calculado
    potion_score     = Column(Float)                                # 0-100
    digestion_delta  = Column(Float)                                # variacao na digestao

    created_at       = Column(DateTime, default=datetime.utcnow)
    beyonder         = relationship("Beyonder", back_populates="rituals")

class PotionLog(Base):
    # Historico de pocoes ativas
    __tablename__ = "potion_logs"
    id             = Column(String, primary_key=True, default=new_id)
    beyonder_id    = Column(String, ForeignKey("beyonders.id"))
    potion_name    = Column(String, nullable=False)
    ingredients    = Column(JSON)
    started_at     = Column(DateTime, default=datetime.utcnow)
    completed_at   = Column(DateTime)
    success        = Column(Boolean)
    notes          = Column(Text)
    beyonder       = relationship("Beyonder", back_populates="potion_logs")

class Memory(Base):
    # Memoria viva -- compressao de padroes
    __tablename__ = "memories"
    id             = Column(String, primary_key=True, default=new_id)
    beyonder_id    = Column(String, ForeignKey("beyonders.id"))
    period         = Column(String)                                 # week|month|quarter
    period_label   = Column(String)                                 # ex: 2026-W34
    summary        = Column(Text)
    patterns       = Column(JSON)
    shadow_notes   = Column(Text)
    xp_gained      = Column(Float, default=0.0)
    created_at     = Column(DateTime, default=datetime.utcnow)
    beyonder       = relationship("Beyonder", back_populates="memories")
