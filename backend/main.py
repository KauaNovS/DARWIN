from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes import auth, users, sequences, potions, rituals, oracle, memory, health

app = FastAPI(
    title="Darwin API",
    description="Sistema de Evolucao Humana -- Beyonders em ascensao",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api/auth",      tags=["auth"])
app.include_router(users.router,     prefix="/api/users",     tags=["users"])
app.include_router(sequences.router, prefix="/api/sequences", tags=["sequences"])
app.include_router(potions.router,   prefix="/api/potions",   tags=["potions"])
app.include_router(rituals.router,   prefix="/api/rituals",   tags=["rituals"])
app.include_router(oracle.router,    prefix="/api/oracle",    tags=["oracle"])
app.include_router(memory.router,    prefix="/api/memory",    tags=["memory"])
app.include_router(health.router,    prefix="/api/health",    tags=["health"])

@app.get("/")
async def root():
    return {
        "system": "Darwin",
        "version": "2.0.0",
        "message": "O caminho se abre para quem ousa caminhar.",
    }
