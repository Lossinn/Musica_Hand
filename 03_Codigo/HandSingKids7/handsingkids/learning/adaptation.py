"""Motor adaptativo por reglas.

Decide qué hacer después de cada actividad. Trabaja sobre un retrato del estado
del niño —dominio por habilidad, desempeño reciente, fatiga estimada y repasos
vencidos— y devuelve una decisión, no una pantalla: quién la ejecuta es asunto
de la capa de aplicación.

La escalera de ayuda, cuando algo va mal, no consiste en repetir lo mismo más
veces: se baja el tempo, se acorta la secuencia, se muestra la seña, se aísla la
nota que falla y solo entonces se vuelve a la secuencia completa.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum

from ..domain.entities import (Activity, ActivityKind, PlayMode, Skill,
                               SkillState, SkillStatus)
from ..domain.notes import solfa


class Decision(str, Enum):
    REPEAT = "repetir"              # la misma actividad otra vez
    EASE_DOWN = "bajar"             # versión más fácil
    MAINTAIN = "mantener"           # otra del mismo nivel
    STEP_UP = "subir"               # más difícil
    INTRODUCE = "introducir"        # habilidad nueva
    REVIEW = "repasar"              # repaso espaciado vencido
    TARGET = "reforzar"             # ejercicio dirigido a una debilidad
    PLAY = "jugar"                  # actividad lúdica, para sostener el ánimo
    ASSESS = "evaluar"              # medir dominio sin ayudas
    REST = "descansar"              # cerrar la sesión


@dataclass
class Context:
    """Retrato del momento, tal como lo ve el motor."""
    skill_states: dict[str, SkillState]
    skills: dict[str, Skill]
    last_accuracy: float = 100.0            # 0..100 de la última actividad
    consecutive_failures: int = 0           # actividades seguidas por debajo del umbral
    activities_in_session: int = 0
    minutes_in_session: float = 0.0
    session_budget_min: int = 8
    age_band: str = "medianos"
    last_kinds: list[ActivityKind] = field(default_factory=list)

    @property
    def fatigue(self) -> float:
        """Fatiga estimada en [0, 1]: mezcla cuánto lleva jugado y cuánto tiempo.

            F = clip( 0.5 * n/N + 0.5 * t/T )
        """
        by_count = self.activities_in_session / max(1, self.session_budget_min / 2)
        by_time = self.minutes_in_session / max(1, self.session_budget_min)
        return max(0.0, min(1.0, 0.5 * by_count + 0.5 * by_time))

    def due_reviews(self, now: float | None = None) -> list[str]:
        now = now if now is not None else time.time()
        return [code for code, st in self.skill_states.items()
                if st.due_at > 0 and now >= st.due_at
                and st.status != SkillStatus.LOCKED]

    def weakest(self, limit: int = 3) -> list[str]:
        activos = [(c, s) for c, s in self.skill_states.items()
                   if s.status in (SkillStatus.INTRODUCED, SkillStatus.PRACTICING)
                   and s.attempts > 0]
        activos.sort(key=lambda t: t[1].mastery)
        return [c for c, _ in activos[:limit]]

    def ready_to_unlock(self) -> list[str]:
        """Habilidades bloqueadas cuyos prerrequisitos ya están dominados."""
        out = []
        for code, skill in self.skills.items():
            st = self.skill_states.get(code)
            if st is None or st.status != SkillStatus.LOCKED:
                continue
            if all(self.skill_states.get(p, SkillState(0, p)).status
                   in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED)
                   for p in skill.prerequisites):
                out.append(code)
        return out


@dataclass
class Plan:
    decision: Decision
    reason: str
    skill_code: str | None = None
    tempo_factor: float = 1.0
    length_factor: float = 1.0
    force_hints: bool = False


# Escalera de ayuda: cada peldaño retira una exigencia distinta.
SCAFFOLD = (
    Plan(Decision.EASE_DOWN, "Bajamos el ritmo para que dé tiempo",
         tempo_factor=0.80),
    Plan(Decision.EASE_DOWN, "Acortamos la secuencia", tempo_factor=0.80,
         length_factor=0.6),
    Plan(Decision.EASE_DOWN, "Mostramos la seña mientras practica",
         tempo_factor=0.75, length_factor=0.6, force_hints=True),
    Plan(Decision.TARGET, "Practicamos sola la nota que cuesta",
         tempo_factor=0.75, length_factor=0.5, force_hints=True),
)


class AdaptationEngine:
    """Reglas explícitas. La versión con optimización y aprendizaje por refuerzo
    se apoya en este mismo contexto, de modo que puede sustituirla sin tocar el
    resto del sistema."""

    def __init__(self, mastery_threshold: float = 0.80,
                 struggle_accuracy: float = 55.0,
                 comfort_accuracy: float = 88.0) -> None:
        self.mastery_threshold = mastery_threshold
        self.struggle_accuracy = struggle_accuracy
        self.comfort_accuracy = comfort_accuracy

    def decide(self, ctx: Context) -> Plan:
        # 1. Sesión agotada: mejor parar en alto que insistir.
        if ctx.fatigue >= 1.0:
            return Plan(Decision.REST, "Ya practicaste bastante por hoy")

        # 2. Dificultad sostenida: se baja por la escalera de ayuda.
        if ctx.consecutive_failures >= 1 and ctx.last_accuracy < self.struggle_accuracy:
            peldano = min(ctx.consecutive_failures - 1, len(SCAFFOLD) - 1)
            plan = SCAFFOLD[peldano]
            weak = ctx.weakest(1)
            return Plan(plan.decision, plan.reason,
                        skill_code=weak[0] if weak else None,
                        tempo_factor=plan.tempo_factor,
                        length_factor=plan.length_factor,
                        force_hints=plan.force_hints)

        # 3. Cansancio a media sesión: una actividad lúdica sostiene el ánimo.
        if ctx.fatigue >= 0.7 and ActivityKind.GAME not in ctx.last_kinds[-2:]:
            return Plan(Decision.PLAY, "Un juego para cerrar con energía")

        # 4. Repasos vencidos: tienen prioridad sobre avanzar.
        vencidos = ctx.due_reviews()
        if vencidos:
            peor = min(vencidos,
                       key=lambda c: ctx.skill_states[c].mastery)
            return Plan(Decision.REVIEW, "Toca repasar algo de antes",
                        skill_code=peor)

        # 5. Todo cómodo y hay algo nuevo por abrir.
        if ctx.last_accuracy >= self.comfort_accuracy:
            nuevas = ctx.ready_to_unlock()
            if nuevas:
                return Plan(Decision.INTRODUCE, "¡Lista una seña nueva!",
                            skill_code=nuevas[0])
            return Plan(Decision.STEP_UP, "Vamos por algo un poco más difícil")

        # 6. Hay una debilidad clara pero no está fallando: refuerzo dirigido.
        debiles = ctx.weakest(1)
        if debiles and ctx.skill_states[debiles[0]].mastery < self.mastery_threshold * 0.8:
            return Plan(Decision.TARGET, "Reforzamos lo que todavía cuesta",
                        skill_code=debiles[0])

        return Plan(Decision.MAINTAIN, "Seguimos practicando")


# ---------------------------------------------- generación de actividades

def ease_activity(activity: Activity, plan: Plan) -> Activity:
    """Produce una variante más suave de una actividad existente."""
    seq = list(activity.sequence)
    if plan.length_factor < 1.0 and len(seq) > 2:
        seq = seq[:max(2, int(round(len(seq) * plan.length_factor)))]
    tempo = max(45, int(activity.tempo_bpm * plan.tempo_factor))
    return Activity(
        code=f"{activity.code}__facil",
        kind=activity.kind, title=activity.title, level=activity.level,
        difficulty=max(0.05, activity.difficulty * 0.7),
        skill_codes=list(activity.skill_codes), sequence=seq,
        mode=PlayMode.GUIDED if plan.force_hints else activity.mode,
        tempo_bpm=tempo, duration_s=activity.duration_s,
        hints=True if plan.force_hints else activity.hints,
        repetitions=1, description=plan.reason, icon=activity.icon,
        tolerance_ms=int(activity.tolerance_ms * 1.4))


def targeted_activity(weak_note: str, anchor_note: str | None, level: int,
                      length: int = 6, tempo: int = 64) -> Activity:
    """Ejercicio dirigido a una nota concreta.

    La nota débil se intercala con una ya dominada, que sirve de referencia:
    alternar obliga a distinguirlas, que es justo lo que falla cuando dos señas
    se confunden. Si no hay ninguna dominada, se repite la débil sola.
    """
    if anchor_note and anchor_note != weak_note:
        seq = []
        for i in range(length):
            seq.append(weak_note if i % 2 == 0 else anchor_note)
        # Cierra con la nota débil para que la última impresión sea esa.
        seq[-1] = weak_note
    else:
        seq = [weak_note] * length

    return Activity(
        code=f"dirigido_{weak_note}",
        kind=ActivityKind.REVIEW,
        title=f"Practiquemos {solfa(weak_note)}",
        level=level, difficulty=0.30,
        skill_codes=[f"nota_{weak_note}"], sequence=seq,
        mode=PlayMode.GUIDED, tempo_bpm=tempo,
        duration_s=max(30, int(length * 2.4)), hints=True, repetitions=1,
        description=f"Un ejercicio corto centrado en {solfa(weak_note)}.",
        icon="🎯", tolerance_ms=3200)


def pick_anchor(ctx: Context, weak_skill: str) -> str | None:
    """Elige una nota dominada que sirva de contraste."""
    candidatos = [c for c, s in ctx.skill_states.items()
                  if c != weak_skill and c.startswith("nota_")
                  and s.status in (SkillStatus.MASTERED, SkillStatus.CONSOLIDATED)]
    if not candidatos:
        candidatos = [c for c, s in ctx.skill_states.items()
                      if c != weak_skill and c.startswith("nota_")
                      and s.mastery > 0.5]
    if not candidatos:
        return None
    mejor = max(candidatos, key=lambda c: ctx.skill_states[c].mastery)
    return mejor.replace("nota_", "")


def shuffled_variant(activity: Activity, seed: int | None = None) -> Activity:
    """Misma dificultad, distinto orden: evita que el niño memorice la
    secuencia en lugar de aprender las señas."""
    rng = random.Random(seed)
    seq = list(activity.sequence)
    if len(seq) > 2:
        rng.shuffle(seq)
    return Activity(
        code=f"{activity.code}__var", kind=activity.kind, title=activity.title,
        level=activity.level, difficulty=activity.difficulty,
        skill_codes=list(activity.skill_codes), sequence=seq,
        mode=activity.mode, tempo_bpm=activity.tempo_bpm,
        duration_s=activity.duration_s, hints=activity.hints,
        repetitions=activity.repetitions, description=activity.description,
        icon=activity.icon, tolerance_ms=activity.tolerance_ms)
