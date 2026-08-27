# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, users, tasks, agents, memory, graph, evolution, health, instinct
from core.config import settings

app = FastAPI(
    title="Darwin Genesis API",
    description="Sistema Operacional de Evolução Humana",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(memory.router, prefix="/api/memory", tags=["memory"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(evolution.router, prefix="/api/evolution", tags=["evolution"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(instinct.router, prefix="/api/instinct", tags=["instinct"])

@app.get("/")
async def root():
    return {"message": "Darwin Genesis API", "version": "0.1.0"}
