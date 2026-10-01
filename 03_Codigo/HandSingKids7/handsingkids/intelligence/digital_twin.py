"""Gemelo digital del aprendiz.

Es la representación del estado de aprendizaje de un niño en un momento dado:
qué domina, qué le cuesta, qué confunde con qué, cómo viene evolucionando y qué
conviene hacer a continuación. El motor adaptativo y el optimizador leen de aquí;
la Zona de Padres muestra esto mismo traducido a lenguaje llano.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..domain.entities import Profile, Skill, SkillState, SkillStatus
from ..domain.notes import NOTE_CODES, solfa
from ..learning import mastery as M

DIA = 86400.0


@dataclass
class SkillSnapshot:
    code: str
    name: str
    note_code: str | None
    status: SkillStatus
    mastery: float
    precision: float
    consistency: float
    speed: float
    retention: float
    attempts: int
    days_since_practice: float
    due_in_days: float

    @property
    def label(self) -> str:
        return solfa(self.note_code) if self.note_code else self.name

    @property
    def is_weak(self) -> bool:
        return self.attempts > 0 and self.mastery < 0.55

    @property
    def is_strong(self) -> bool:
        return self.mastery >= M.MASTERED_AT


@dataclass
class DigitalTwin:
    profile: Profile
    skills: list[SkillSnapshot] = field(default_factory=list)
    confusions: list[tuple[str, str, int]] = field(default_factory=list)
    weekly_minutes: float = 0.0
    weekly_activities: int = 0
    trend: float = 0.0          # variación de precisión respecto a la semana previa
    total_attempts: int = 0
    generated_at: float = field(default_factory=time.time)

    # ------------------------------------------------------------ lecturas
    @property
    def overall_mastery(self) -> float:
        practicadas = [s for s in self.skills if s.attempts > 0]
        if not practicadas:
            return 0.0
        return sum(s.mastery for s in practicadas) / len(practicadas)

    @property
    def strengths(self) -> list[SkillSnapshot]:
        return sorted([s for s in self.skills if s.is_strong],
                      key=lambda s: -s.mastery)

    @property
    def weaknesses(self) -> list[SkillSnapshot]:
        return sorted([s for s in self.skills if s.is_weak],
                      key=lambda s: s.mastery)

    @property
    def due(self) -> list[SkillSnapshot]:
        return sorted([s for s in self.skills if s.due_in_days <= 0
                       and s.status != SkillStatus.LOCKED and s.attempts > 0],
                      key=lambda s: s.due_in_days)

    @property
    def notes_mastered(self) -> list[str]:
        return [s.note_code for s in self.skills
                if s.note_code and s.is_strong]

    def recommendation(self) -> str:
        """Una frase para el adulto, sin jerga."""
        if self.total_attempts == 0:
            return "Todavía no hay práctica registrada. Empiecen por la calibración."
        debiles = self.weaknesses
        if debiles:
            nombres = ", ".join(d.label for d in debiles[:2])
            return f"Conviene practicar {nombres} con sesiones cortas y seguidas."
        vencidos = self.due
        if vencidos:
            return (f"Hay {len(vencidos)} seña(s) que llevan días sin repasarse; "
                    "la aplicación las va a proponer sola.")
        if self.overall_mastery >= 0.85:
            return "Va muy bien. Es buen momento para pasar a melodías completas."
        return "El avance es constante. Mantener el ritmo de práctica actual."


def build(profile: Profile, skills: dict[str, Skill],
          states: dict[str, SkillState], *, confusions=None,
          weekly_minutes: float = 0.0, weekly_activities: int = 0,
          trend: float = 0.0, total_attempts: int = 0,
          now: float | None = None) -> DigitalTwin:
    """Arma el gemelo a partir del estado guardado, aplicando el olvido
    acumulado desde la última práctica."""
    now = now if now is not None else time.time()
    snaps: list[SkillSnapshot] = []
    for code, skill in skills.items():
        st = states.get(code) or SkillState(profile.id or 0, code)
        if st.attempts > 0:
            M.decay(st, now=now)
        dias = ((now - st.last_practice_at) / DIA) if st.last_practice_at else 0.0
        vence = ((st.due_at - now) / DIA) if st.due_at else float("inf")
        snaps.append(SkillSnapshot(
            code=code, name=skill.name, note_code=skill.note_code,
            status=st.status, mastery=st.mastery, precision=st.precision,
            consistency=st.consistency, speed=st.speed, retention=st.retention,
            attempts=st.attempts, days_since_practice=round(dias, 2),
            due_in_days=round(vence, 2) if vence != float("inf") else 999.0))
    snaps.sort(key=lambda s: (s.note_code is None,
                              NOTE_CODES.index(s.note_code) if s.note_code
                              in NOTE_CODES else 99))
    return DigitalTwin(profile=profile, skills=snaps,
                       confusions=list(confusions or []),
                       weekly_minutes=weekly_minutes,
                       weekly_activities=weekly_activities, trend=trend,
                       total_attempts=total_attempts, generated_at=now)
