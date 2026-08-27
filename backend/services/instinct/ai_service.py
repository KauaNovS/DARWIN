# services/instinct/ai_service.py
#
# NOVO: gera um insight curto a partir do contexto instintivo do usuário
# (fase de onboarding, estresse, domínio, genoma). Usa a OpenAI se
# OPENAI_API_KEY estiver configurada; caso contrário cai num fallback local
# baseado em regras simples, para nunca quebrar o endpoint por falta de chave.
import httpx
from typing import Dict, Any
from core.config import settings


class AIEngine:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY

    async def generate_insight(self, user_context: Dict[str, Any]) -> str:
        if not self.api_key:
            return self._local_insight(user_context)

        prompt = (
            "Você é o Darwin, um assistente de evolução pessoal.\n"
            f"- Fase: {user_context.get('phase', 'FETUS')}\n"
            f"- Índice de estresse: {user_context.get('stress', 0.5)}\n"
            f"- Domínio atual: {user_context.get('mastery', 0.0)}\n"
            f"- Genoma: {user_context.get('genome', [])}\n"
            "Com base nisso, dê uma recomendação curta (até 3 frases) para "
            "melhorar o bem-estar e a evolução do usuário."
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 150,
                    },
                )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            return self._local_insight(user_context)
        except Exception:
            return self._local_insight(user_context)

    def _local_insight(self, ctx: Dict[str, Any]) -> str:
        stress = ctx.get("stress", 0.5)
        mastery = ctx.get("mastery", 0.0)
        phase = ctx.get("phase", "FETUS")

        if stress > 0.7:
            return "Sugiro uma pausa de 10 minutos para respiração consciente. Sua mente precisa de recuperação."
        if phase == "FETUS":
            return "Você está no início da jornada. Continue respondendo às perguntas diárias para eu aprender sobre você."
        if mastery < 0.3:
            return "Continue praticando e registrando suas atividades. A consistência é a chave para o domínio."
        return "Seu progresso está consistente. Considere aumentar gradualmente a complexidade das suas tarefas."
