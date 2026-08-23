# core/database.py
#
# NOTE: Not present in the original plan document — added as minimal glue
# code so `models/*.py`, `services/graph/*.py` and the automation/IA services
# (which do `from core.database import Base / get_neo4j_driver / get_redis`)
# actually import. Fill in / extend as needed.
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from neo4j import AsyncGraphDatabase
import redis.asyncio as redis_asyncio
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


_neo4j_driver = None


def get_neo4j_driver():
    """Retorna um driver assíncrono do Neo4j (singleton por processo)."""
    global _neo4j_driver
    if _neo4j_driver is None:
        _neo4j_driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    return _neo4j_driver


_redis_client = None


def get_redis():
    """Retorna um cliente assíncrono do Redis (singleton por processo)."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis_asyncio.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client
