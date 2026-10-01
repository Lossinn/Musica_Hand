"""Generación procedural de actividades: contenido que no viene del catálogo fijo.

El catálogo escrito a mano (`data.seed`) tiene un techo: unas sesenta
actividades. Para que la aventura se sienta interminable en vez de dar
vueltas sobre lo mismo, cada vez que `AdventureScreen` arma la ruta del día
también se proponen unas pocas actividades nuevas, generadas sobre la marcha
a partir de las notas que el niño ya tiene abiertas y de las que le cuestan
más — y de esos borradores se elige el que el Agente Adaptativo (el
predictor entrenado con los datos del propio niño, o si aún no hay
suficientes, la fórmula fija) predice más cerca de la dificultad deseable
p* = 0.75, la misma que ya usa `intelligence.optimizer` (Bjork y Bjork,
2011: el aprendizaje no es máximo donde todo sale bien ni donde nada sale).

Solo las que el optimizador termina eligiendo se guardan en la base de datos
(lo hace `AdventureScreen`, no este módulo): así el catálogo crece de verdad
con lo que se llega a jugar, en vez de acumular actividades generadas que
nadie vio.
"""

from __future__ import annotations

import random
import uuid

from ..data.seed import estimate_difficulty
from ..domain.entities import (Activity, ActivityKind, PlayMode, SkillState,
                               SkillStatus)
from ..domain.notes import NOTE_CODES
from ..intelligence.predictor import MasteryPredictor

P_STAR = 0.75

ICONS = ("✨", "🌟", "🎲", "🧩", "🔮")
TEMPO_BASE_POR_NIVEL = {1: 62, 2: 66, 3: 72, 4: 74, 5: 84, 6: 76, 7: 82}
MODOS_CANDIDATOS = (PlayMode.GUIDED, PlayMode.GUIDED, PlayMode.SPEED, PlayMode.MEMORY)


def _notas_disponibles(states: dict[str, SkillState]) -> list[str]:
    return [c for c in NOTE_CODES
            if states.get(f"nota_{c}")
            and states[f"nota_{c}"].status != SkillStatus.LOCKED]


def _notas_flojas(states: dict[str, SkillState], notas: list[str]) -> list[str]:
    activas = [(c, states[f"nota_{c}"]) for c in notas
               if states.get(f"nota_{c}") and states[f"nota_{c}"].attempts > 0]
    activas.sort(key=lambda t: t[1].mastery)
    return [c for c, _ in activas]


def _secuencia_aleatoria(rng: random.Random, notas: list[str],
                         flojas: list[str], largo: int) -> list[str]:
    """Secuencia con más presencia de las notas flojas, sin repetir la misma
    nota dos veces seguidas (eso se sentiría como un error, no como reto)."""
    peso = {c: (3.0 if c in flojas[:2] else 1.0) for c in notas}
    seq: list[str] = []
    anterior = None
    for _ in range(largo):
        candidatos = [c for c in notas if c != anterior] or notas
        pesos = [peso[c] for c in candidatos]
        elegido = rng.choices(candidatos, weights=pesos, k=1)[0]
        seq.append(elegido)
        anterior = elegido
    return seq


def generate_candidates(level: int, states: dict[str, SkillState],
                        predictor: MasteryPredictor, *, n: int = 6,
                        seed: int | None = None) -> list[Activity]:
    """Propone hasta `n` actividades nuevas para ese nivel.

    Devuelve una lista vacía si todavía no hay al menos dos notas abiertas
    (no tiene sentido "generar variedad" con una sola seña)."""
    rng = random.Random(seed)
    notas = _notas_disponibles(states)
    if len(notas) < 2:
        return []
    flojas = _notas_flojas(states, notas)
    tempo_base = TEMPO_BASE_POR_NIVEL.get(level, 72)

    candidatas: list[Activity] = []
    for _ in range(n):
        largo = rng.randint(3, min(7, 3 + level))
        modo = rng.choice(MODOS_CANDIDATOS)
        tempo = max(48, tempo_base + rng.randint(-8, 14))
        pistas = True

        # Tres borradores de secuencia; se elige el que el agente adaptativo
        # predice más cerca de p* (ni tan fácil que aburra, ni tan difícil
        # que frustre) en vez de tomar el primero al azar.
        mejor_seq: list[str] | None = None
        mejor_dif = 0.3
        mejor_dist = float("inf")
        for _ in range(3):
            seq = _secuencia_aleatoria(rng, notas, flojas, largo)
            dificultad = estimate_difficulty(seq, modo, pistas, tempo)
            borrador = Activity(
                code="_borrador", kind=ActivityKind.EXERCISE, title="",
                level=level, difficulty=dificultad,
                skill_codes=sorted({f"nota_{c}" for c in seq}), sequence=seq,
                mode=modo, tempo_bpm=tempo,
                duration_s=max(20, int(largo * (60.0 / tempo) * 2.2) + 10),
                hints=pistas, repetitions=1)
            p = predictor.probability(borrador, states).probability
            dist = abs(p - P_STAR)
            if dist < mejor_dist:
                mejor_seq, mejor_dif, mejor_dist = seq, dificultad, dist

        if not mejor_seq:
            continue

        icono = rng.choice(ICONS)
        dirigida = bool(flojas) and flojas[0] in mejor_seq
        codigo = f"proc_{uuid.uuid4().hex[:10]}"
        candidatas.append(Activity(
            code=codigo,
            kind=ActivityKind.REVIEW if dirigida else ActivityKind.EXERCISE,
            title=f"Reto de Kiki {icono}", level=level, difficulty=mejor_dif,
            skill_codes=sorted({f"nota_{c}" for c in mejor_seq}),
            sequence=mejor_seq, mode=modo, tempo_bpm=tempo,
            duration_s=max(20, int(len(mejor_seq) * (60.0 / tempo) * 2.2) + 10),
            hints=pistas, repetitions=1,
            description="Generado para ti por el Agente Adaptativo, a partir "
                        "de tu propio progreso.",
            icon=icono, tolerance_ms=2600))
    return candidatas
