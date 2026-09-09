"""Perfil de aprendizaje del niño (Fases 5–6).

Vector de estado (§11):
    S_t = (P_t, E_t, T_t, R_t, D_t, M_t)
      P_t = precisión
      E_t = cantidad de errores
      T_t = tiempo de respuesta
      R_t = ritmo / progreso
      D_t = dificultad actual
      M_t = nivel de dominio musical

Transición:  S_(t+1) = F(S_t, A_t, O_t)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .. import config


@dataclass
class StateVector:
    """S_t. Todos los valores normalizados a [0, 1] salvo dificultad (1..5)."""

    precision: float = 0.0
    errores: float = 0.0
    tiempo_respuesta: float = 0.0
    progreso: float = 0.0
    dificultad: int = config.DIFICULTAD_MIN
    dominio: float = 0.0

    def as_tuple(self) -> tuple[float, float, float, float, int, float]:
        return (
            self.precision,
            self.errores,
            self.tiempo_respuesta,
            self.progreso,
            self.dificultad,
            self.dominio,
        )


class ChildProfile:
    """Estado + historial de un niño. Persistible en data/users/<id>.json."""

    def __init__(self, user_id: str = "default", edad: int = 7) -> None:
        self.user_id = user_id
        self.edad = edad
        self.state = StateVector()
        self.history: list[dict] = []          # lista de ActivityResult serializados
        # métricas derivadas (§10)
        self.nota_dominada: str | None = None
        self.nota_dificil: str | None = None
        self.nivel: int = 1
        self.tendencia: str = "estable"        # "mejorando" | "estable" | "empeorando"

    # ── actualización:  S_(t+1) = F(S_t, A_t, O_t) ──────────────────────
    def update(self, result) -> StateVector:
        """Incorpora un ActivityResult y recalcula el vector de estado."""
        raise NotImplementedError("Fase 6: recalcular S_t desde el historial")

    # ── KPIs (§32) ─────────────────────────────────────────────────────
    def accuracy(self) -> float:
        """Predicciones correctas / totales."""
        raise NotImplementedError

    def mean_response_time(self) -> float:
        raise NotImplementedError

    def error_rate(self) -> float:
        raise NotImplementedError

    # ── persistencia ───────────────────────────────────────────────────
    def path(self) -> Path:
        return config.USERS_DIR / f"{self.user_id}.json"

    def save(self) -> None:
        raise NotImplementedError("Fase 5: guardar perfil + historial")

    @classmethod
    def load(cls, user_id: str) -> "ChildProfile":
        raise NotImplementedError("Fase 5: cargar perfil")
