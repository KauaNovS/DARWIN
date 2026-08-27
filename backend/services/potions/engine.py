from datetime import date, datetime
from models.beyonder import Ritual, Beyonder
from services.sequences.paths import get_sequence_for_beyonder

# Pesos de cada ingrediente no score da pocao
# Definidos pelos especialistas: psicologos, nutris, terapeutas
INGREDIENT_WEIGHTS = {
    # Fisicos -- base bioquimica (35% do total)
    "sleep_hours":         {"max": 9.0,  "weight": 0.10, "ideal": 8.0},
    "sleep_quality":       {"max": 10.0, "weight": 0.08, "ideal": 8.0},
    "water_ml":            {"max": 3000, "weight": 0.05, "ideal": 2500},
    "nutrition_score":     {"max": 10.0, "weight": 0.07, "ideal": 8.0},
    "movement_minutes":    {"max": 90.0, "weight": 0.05, "ideal": 45.0},

    # Cognitivos -- plasticidade e crescimento (30% do total)
    "reading_minutes":     {"max": 60.0, "weight": 0.10, "ideal": 30.0},
    "meditation_minutes":  {"max": 45.0, "weight": 0.10, "ideal": 20.0},
    "journaling":          {"max": 1.0,  "weight": 0.10, "ideal": 1.0},

    # Emocionais -- regulacao e conexao (35% do total)
    "emotional_state":     {"max": 10.0, "weight": 0.12, "ideal": 7.0},
    "anxiety_level":       {"max": 10.0, "weight": 0.12, "invert": True, "ideal": 3.0},
    "social_connection":   {"max": 10.0, "weight": 0.11, "ideal": 7.0},
}

def calculate_potion_score(ritual: Ritual) -> float:
    total = 0.0
    for field, cfg in INGREDIENT_WEIGHTS.items():
        val = getattr(ritual, field, None)
        if val is None:
            continue
        normalized = float(val) / cfg["max"]
        if cfg.get("invert"):
            normalized = 1.0 - normalized
        normalized = max(0.0, min(1.0, normalized))
        total += normalized * cfg["weight"]
    # Bonus por consistencia de anotacoes (insight e gratidao)
    if ritual.insights:
        total += 0.02
    if ritual.gratitude:
        total += 0.02
    return round(min(total * 100, 100), 2)

def calculate_digestion_delta(potion_score: float, current_digestion: float) -> float:
    # A digestao e lenta -- mudancas bruscas nao sao reais
    # Inspirado em curvas de aprendizado de psicologia cognitiva
    base_delta = (potion_score - current_digestion) * 0.08
    # Penalidade se score muito baixo (resistencia)
    if potion_score < 30:
        base_delta *= 0.5
    # Bonus se consistencia alta
    if potion_score >= 80:
        base_delta *= 1.2
    return round(base_delta, 3)

def check_level_advancement(beyonder: Beyonder) -> dict:
    seq = get_sequence_for_beyonder(beyonder.path, beyonder.sequence_level)
    if not seq:
        return {"can_advance": False, "reason": "Sequencia nao encontrada"}

    threshold = seq.get("digestion_threshold", 100.0)
    xp_required = seq.get("xp_required", 99999)

    if beyonder.digestion_score < threshold:
        return {
            "can_advance": False,
            "reason": f"Digestao atual: {beyonder.digestion_score:.1f}% / {threshold}% necessario",
            "progress": round((beyonder.digestion_score / threshold) * 100, 1),
        }
    if beyonder.total_xp < xp_required:
        return {
            "can_advance": False,
            "reason": f"XP atual: {beyonder.total_xp:.0f} / {xp_required} necessario",
            "progress": round((beyonder.total_xp / xp_required) * 100, 1),
        }
    return {
        "can_advance": True,
        "current_level": beyonder.sequence_level,
        "next_level": beyonder.sequence_level - 1,
    }

def calculate_xp_for_ritual(ritual: Ritual, potion_score: float) -> float:
    base_xp = potion_score * 0.5          # Max 50 XP por ritual perfeito
    if ritual.journaling:
        base_xp += 5
    if ritual.insights and len(ritual.insights) > 50:
        base_xp += 5
    if ritual.gratitude and len(ritual.gratitude) > 20:
        base_xp += 3
    return round(base_xp, 2)

def analyze_shadow(rituals: list) -> dict:
    # Analise de padroes de sombra -- principios junguianos aplicados
    # Detecta comportamentos automaticos e evitamentos
    if len(rituals) < 7:
        return {"shadow_index": 0.0, "patterns": [], "notes": "Dados insuficientes"}

    anxiety_avg = sum(r.anxiety_level or 5 for r in rituals[-7:]) / 7
    journaling_rate = sum(1 for r in rituals[-7:] if r.journaling) / 7
    social_avg = sum(r.social_connection or 5 for r in rituals[-7:]) / 7
    emotional_avg = sum(r.emotional_state or 5 for r in rituals[-7:]) / 7

    shadow_index = 0.0
    patterns = []
    notes_parts = []

    # Alta ansiedade + baixo journaling = material inconsciente acumulando
    if anxiety_avg > 6 and journaling_rate < 0.4:
        shadow_index += 25.0
        patterns.append("ansiedade_nao_processada")
        notes_parts.append(
            "Alta ansiedade combinada com baixa expressao escrita sugere "
            "material emocional nao integrado. Aumente o journaling."
        )

    # Baixa conexao social + baixo estado emocional = isolamento
    if social_avg < 4 and emotional_avg < 5:
        shadow_index += 20.0
        patterns.append("isolamento_defensivo")
        notes_parts.append(
            "Padrao de isolamento detectado. O isolamento e uma defesa comum "
            "que bloqueia a digestao emocional. Busque conexao, mesmo que pequena."
        )

    # Estado emocional muito variavel (instabilidade)
    emotional_vals = [r.emotional_state or 5 for r in rituals[-7:]]
    if max(emotional_vals) - min(emotional_vals) > 5:
        shadow_index += 15.0
        patterns.append("instabilidade_emocional")
        notes_parts.append(
            "Variabilidade emocional alta. Isso pode indicar gatilhos nao identificados. "
            "Preste atencao ao que acontece nos dias de pico e de vale."
        )

    return {
        "shadow_index": min(shadow_index, 100.0),
        "patterns": patterns,
        "notes": " | ".join(notes_parts) if notes_parts else "Sem padroes de sombra detectados.",
    }
