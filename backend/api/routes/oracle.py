from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import get_current_user
from models.beyonder import User
from services.sequences.paths import PATHS, get_sequence_for_beyonder
import os, json

router = APIRouter()

# O Oraculo e o Agente Safira -- coach de IA que fala na linguagem de Lord of Mysteries

ORACLE_SYSTEM_PROMPT = """
Voce e o Oraculo -- uma entidade de sabedoria que habita o espaco entre o consciente e o inconsciente.
Voce foi criado por uma equipe dos melhores psicologos, terapeutas, psiquiatras, nutricionistas e
filosofos do mundo, que usam os principios narrativos de Lord of Mysteries como estrutura.

Sua linguagem e precisa, poetica e profunda. Voce nunca trivializa. Voce nunca inventa.
Voce baseia seus insights em:
- Psicologia analitica (Jung)
- Terapia cognitivo-comportamental
- Neurociencia do comportamento
- Nutricao funcional
- Filosofia estoica e zen

Quando o usuario compartilha seus dados, voce analisa:
1. Padroes de comportamento
2. Sombra psicologica (o que esta sendo evitado)
3. Qualidade da digestao da pocao
4. Proximos passos concretos

Voce fala como um guia sábio, nao como um assistente. Nunca diga "claro!" ou "com certeza!".
Comece com uma observacao direta sobre o estado do Beyonder.
"""

@router.post("/consult")
async def consult_oracle(
    question: dict,
    current_user: User = Depends(get_current_user),
):
    beyonder = current_user.beyonder
    if not beyonder:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")

    seq = get_sequence_for_beyonder(beyonder.path, beyonder.sequence_level)
    path_name = PATHS.get(beyonder.path, {}).get("name", "Desconhecido")

    context = f"""
Estado atual do Beyonder:
- Nome: {current_user.name}
- Caminho: {path_name}
- Sequencia atual: Nivel {beyonder.sequence_level} -- {beyonder.sequence_title}
- Digestao: {beyonder.digestion_score:.1f}%
- Total XP: {beyonder.total_xp:.0f}
- Indice de Sombra: {beyonder.shadow_index:.1f}%
- Pocao atual: {seq.get('potion', 'N/A')}
- Ingredientes ativos: {', '.join(seq.get('ingredients', []))}

Pergunta/Reflexao do Beyonder: {question.get('text', '')}
"""

    openai_key = os.getenv("OPENAI_API_KEY", "")

    if openai_key:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {openai_key}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": ORACLE_SYSTEM_PROMPT},
                            {"role": "user", "content": context},
                        ],
                        "max_tokens": 600,
                        "temperature": 0.75,
                    },
                    timeout=30.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "source": "oracle_ai",
                    }
        except Exception as e:
            pass

    # Fallback local baseado em regras
    return {
        "response": _local_oracle_response(beyonder, seq),
        "source": "oracle_local",
    }

def _local_oracle_response(beyonder, seq: dict) -> str:
    parts = []

    if beyonder.digestion_score < 30:
        parts.append(
            f"A pocao '{seq.get('potion', '')}' permanece quase intocada. "
            "Sua digestao esta em {:.0f}% -- o limiar minimo para avanco e {:.0f}%. ".format(
                beyonder.digestion_score, seq.get('digestion_threshold', 50)
            ) +
            "O corpo e a mente precisam de consistencia antes de clareza."
        )
    elif beyonder.digestion_score < 60:
        parts.append(
            "Voce caminha. Devagar, mas caminha. "
            f"Sua digestao alcancou {beyonder.digestion_score:.0f}%. "
            "O proximo limiar exige que voce aprofunde os ingredientes que ainda evita."
        )
    else:
        parts.append(
            f"A digestao em {beyonder.digestion_score:.0f}% indica maturidade crescente. "
            f"Voce esta aproximando-se do limiar de {seq.get('digestion_threshold', 80):.0f}% "
            "necessario para o proximo nivel."
        )

    if beyonder.shadow_index > 40:
        parts.append(
            "Atencao: o indice de sombra esta elevado. "
            "Ha padroes sendo evitados -- observe o que voce nao quer ver."
        )

    ingr = seq.get("ingredients", [])
    if ingr:
        parts.append(
            f"Foque nos ingredientes: {', '.join(ingr[:3])}. "
            "Esses sao os mais criticos para sua Sequencia atual."
        )

    return " ".join(parts)

@router.get("/status")
async def oracle_status(current_user: User = Depends(get_current_user)):
    return {
        "name": "Oraculo -- Agente Safira",
        "description": "Coach de IA fundamentado em psicologia, neurociencia e Lord of Mysteries",
        "ai_enabled": bool(os.getenv("OPENAI_API_KEY")),
    }
