"""Progresión por niveles y estado del mapa musical."""

from __future__ import annotations

from dataclasses import dataclass

from ..data.seed import LEVELS
from ..domain.entities import Skill, SkillState, SkillStatus

# Estrellas necesarias, como fracción del máximo del nivel, para abrir el
# siguiente. Con 0.55 basta con hacerlo razonablemente bien, no a la perfección.
UNLOCK_RATIO = 0.55


@dataclass
class LevelState:
    level: int
    title: str
    subtitle: str
    icon: str
    color: str
    unlocked: bool
    completed: bool
    stars: int
    max_stars: int

    @property
    def ratio(self) -> float:
        return self.stars / self.max_stars if self.max_stars else 0.0


def level_states(activities, stars_by_activity: dict[str, int]) -> list[LevelState]:
    """Construye el estado de cada nivel a partir de las estrellas obtenidas."""
    por_nivel: dict[int, list] = {}
    for a in activities:
        por_nivel.setdefault(a.level, []).append(a)

    estados: list[LevelState] = []
    anterior_abierto = True
    for meta in LEVELS:
        lvl = meta["level"]
        acts = por_nivel.get(lvl, [])
        max_stars = 3 * len(acts)
        stars = sum(min(3, stars_by_activity.get(a.code, 0)) for a in acts)
        unlocked = anterior_abierto
        completed = max_stars > 0 and stars >= UNLOCK_RATIO * max_stars
        estados.append(LevelState(
            level=lvl, title=meta["title"], subtitle=meta["subtitle"],
            icon=meta["icon"], color=meta["color"], unlocked=unlocked,
            completed=completed, stars=stars, max_stars=max_stars))
        anterior_abierto = completed
    return estados


def current_level(estados: list[LevelState]) -> int:
    for e in estados:
        if e.unlocked and not e.completed:
            return e.level
    return estados[-1].level if estados else 1


def unlock_skills(skills: dict[str, Skill],
                  states: dict[str, SkillState]) -> list[str]:
    """Abre las habilidades cuyos prerrequisitos ya están dominados.
    Devuelve los códigos recién abiertos."""
    abiertas: list[str] = []
    for code, skill in skills.items():
        st = states.get(code)
        if st is None or st.status != SkillStatus.LOCKED:
            continue
        if all(states.get(p) is not None
               and states[p].status in (SkillStatus.MASTERED,
                                        SkillStatus.CONSOLIDATED)
               for p in skill.prerequisites):
            st.status = SkillStatus.INTRODUCED
            abiertas.append(code)
    return abiertas
