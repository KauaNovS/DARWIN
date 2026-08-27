# models/genome.py
#
# Não é uma tabela SQL: o Genoma é um resumo comprimido (JSON) guardado no
# Redis pelo GeneticMemory, então aqui só definimos o formato dos dados.
from typing import List
from datetime import datetime
from pydantic import BaseModel


class Trait(BaseModel):
    name: str
    value: float
    confidence: float = 0.7
    source: str = "genetic_memory"


class Genome(BaseModel):
    user_id: str
    traits: List[Trait]
    compress_count: int = 0
    last_compressed_at: datetime = datetime.utcnow()
    raw_events_archived: int = 0
