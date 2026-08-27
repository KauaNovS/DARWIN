# services/instinct/sentinel.py
#
# CORRIGIDO: (1) importava de `app.core.database`, inexistente — usa
# `core.database.get_redis()`. (2) `get_days_active()` no scaffold original
# contava chaves de resposta (uma por pergunta) como se fossem dias, então
# 1 dia com 3 respostas virava "3 dias ativos" — inflava a fase de onboarding
# artificialmente. Agora cada dia grava uma chave própria carimbada com a
# data (`YYYY-MM-DD`), então a contagem reflete dias reais, não respostas.
from typing import Dict, Any
from datetime import datetime
from core.database import get_redis


class OnboardingSentinel:
    """
    Fase Feto: primeiros 7 dias, Darwin age apenas como Diário Sentinela.
    Só libera complexidade quando a confiança (dias ativos) é suficiente.
    """

    QUESTION_KEYS = ["energy", "focus", "conclusion"]

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis = get_redis()
        self.phase_key = f"onboarding:phase:{user_id}"
        self.start_key = f"onboarding:start:{user_id}"
        self.daily_key = f"onboarding:daily:{user_id}"

    async def get_phase(self) -> str:
        phase = await self.redis.get(self.phase_key)
        return phase or "FETUS"

    async def start_onboarding(self) -> Dict[str, Any]:
        already_started = await self.redis.get(self.start_key)
        if not already_started:
            await self.redis.setex(self.start_key, 86400 * 365, "started")
            await self.redis.setex(self.phase_key, 86400 * 365, "FETUS")
        return {
            "phase": await self.get_phase(),
            "message": "Bem-vindo ao Darwin. Nos próximos 7 dias, vou apenas observar e aprender.",
            "questions": self.get_daily_questions(),
        }

    def get_daily_questions(self) -> list:
        return [
            "Como está sua energia hoje? (0-10)",
            "O que te tirou o foco hoje?",
            "O que você concluiu hoje?",
        ]

    async def record_daily_answer(self, question_key: str, answer: str) -> None:
        """Registra a resposta do dia e marca o dia como ativo."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        answer_key = f"{self.daily_key}:{today}:{question_key}"
        await self.redis.setex(answer_key, 86400 * 90, answer)

        day_key = f"{self.daily_key}:days:{today}"
        await self.redis.setex(day_key, 86400 * 90, "1")

    async def get_days_active(self) -> int:
        """Conta dias distintos com pelo menos uma resposta registrada."""
        pattern = f"{self.daily_key}:days:*"
        keys = await self.redis.keys(pattern)
        return len(keys)

    async def advance_phase(self) -> Dict[str, Any]:
        phase = await self.get_phase()
        days_active = await self.get_days_active()

        if phase == "FETUS" and days_active >= 7:
            await self.redis.setex(self.phase_key, 86400 * 365, "INFANT")
            return {
                "phase": "INFANT",
                "unlocked": ["tarefas_prioridade", "grafo_simples"],
                "message": "Eu notei seus padrões. Vamos começar sua primeira Sequência de evolução.",
            }

        if phase == "INFANT" and days_active >= 30:
            await self.redis.setex(self.phase_key, 86400 * 365, "ADULT")
            return {
                "phase": "ADULT",
                "unlocked": ["agentes", "automacoes", "sequencias_completas", "empresas"],
                "message": "Você está pronto para a versão completa do Darwin.",
            }

        return {"phase": phase, "days_active": days_active}
