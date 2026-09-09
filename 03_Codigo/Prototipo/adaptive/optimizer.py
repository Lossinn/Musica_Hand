"""Optimización de asignación de actividades (Fase 7) — MILP con PuLP.

Pregunta (§12): ¿qué actividad, en qué momento y con qué dificultad, dado el
desempeño, el progreso y las restricciones de la sesión?

Variable de decisión (§12):
    x[n,a,d,t] ∈ {0,1}   = 1 si al niño n se le asigna la actividad a
                            con dificultad d en el periodo t

Función objetivo (§13):
    max Z = α·L + β·P + γ·M − δ·E − ε·T

Restricciones (§14):
    · cada periodo tiene exactamente una actividad:  Σ_{a,d} x[n,a,d,t] = 1
    · límite de sesión:  Σ Dur[a,d,t]·x[n,a,d,t] ≤ T_max
    · dificultad máxima, repeticiones, nº de notas, variedad, progresión...
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .. import config, curriculum


@dataclass
class SessionConstraints:
    """Restricciones de la sesión actual.

    Se construye desde un `adapter.MargenAccion`: el MILP nunca elige notas,
    figuras o dificultades fuera de lo que el currículo y el progreso permiten.
    """

    t_max_s: float = 300.0
    periodos: int = 6
    dificultad_max: int = config.DIFICULTAD_MAX
    max_repeticiones_nota: int = 3
    min_variedad_dinamicas: int = 2
    notas_disponibles: tuple[str, ...] = config.NOTAS
    figuras_disponibles: tuple[str, ...] = ()
    dinamicas_disponibles: tuple[str, ...] = config.DINAMICAS
    max_notas_nuevas: int = 1
    notas_a_reforzar: tuple[str, ...] = ()

    @classmethod
    def desde_margen(cls, margen, t_max_s: float = 300.0, periodos: int = 6) -> "SessionConstraints":
        """Traduce `adapter.MargenAccion` -> restricciones del MILP."""
        raise NotImplementedError("Fase 7: MargenAccion -> SessionConstraints")


class ActivityOptimizer:
    """Construye y resuelve el MILP de asignación de actividades."""

    def __init__(self, weights: dict | None = None) -> None:
        self.weights = weights or dict(config.MILP_WEIGHTS)

    def build_model(self, profile, prediction, constraints: SessionConstraints):
        """Crea el pulp.LpProblem con variables, objetivo y restricciones."""
        raise NotImplementedError("Fase 7: formular MILP con PuLP")

    def solve(self, profile, prediction, constraints: SessionConstraints | None = None):
        """Resuelve y devuelve el plan de la sesión (lista de Activity)."""
        raise NotImplementedError("Fase 7: resolver MILP")

    def select(self, profile, prediction, constraints: SessionConstraints | None = None):
        """Atajo: devuelve solo la SIGUIENTE actividad del plan óptimo."""
        raise NotImplementedError("Fase 7: primera actividad del plan")
