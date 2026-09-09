"""Calibración — FOCO DEL TRABAJO ACTUAL (Fase 4).

No se cambian las notas, formas ni ubicaciones que ya funcionan.
Solo cambia *cómo se obtiene* la calibración:

    Antes:  ubicaciones definidas manualmente -> configuración -> reconocimiento
    Ahora:  inicio -> detección automática -> identificación de posiciones
            -> calibración -> almacenamiento -> reconocimiento

Modelo (§9):
    C = f(H)            H = características observadas de la mano
                        C = configuración calibrada
    G = f(H, C)         durante el juego
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import config


@dataclass
class CalibrationProfile:
    """Configuración calibrada `C`. Serializable a/desde JSON."""

    user_id: str
    # referencia por nota: vector de características normalizadas de la mano
    references: dict[str, list[float]] = field(default_factory=dict)
    # metadatos de la mano del usuario (escala, etc.) para normalización robusta
    hand_scale: float = 1.0
    created_at: str = ""
    version: int = 1

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "CalibrationProfile":
        return cls(**json.loads(text))


class Calibrator:
    """Encuentra y calibra automáticamente las referencias de cada nota.

    Uso previsto:

        calibrator = Calibrator(user_id="nino_01")
        calibrator.load()                 # o -> calibrator.run_auto(vision)
        gesture = calibrator.classify(hand.flat)
    """

    def __init__(self, user_id: str = "default") -> None:
        self.user_id = user_id
        self.profile: CalibrationProfile | None = None

    # ── normalización (independiente de tamaño/distancia/posición, §7) ───
    @staticmethod
    def normalize(landmarks_flat: np.ndarray) -> np.ndarray:
        """Convierte 63 valores crudos en características relativas.

        Centra en la muñeca y escala por el tamaño de la mano para que el
        reconocimiento no dependa de la posición absoluta.
        """
        raise NotImplementedError("Fase 4: normalización relativa de landmarks")

    # ── calibración automática ──────────────────────────────────────────
    def run_auto(self, vision, prompts: list[str] | None = None) -> CalibrationProfile:
        """Guía la calibración automática nota por nota.

        Para cada nota de `config.NOTAS`: detecta la mano estable, promedia
        varias muestras y guarda la referencia normalizada en el perfil.
        """
        raise NotImplementedError("Fase 4: rutina de calibración automática")

    def detect_stable_pose(self, vision, frames: int = 15) -> np.ndarray | None:
        """Espera a que la mano se mantenga quieta y devuelve el promedio."""
        raise NotImplementedError("Fase 4: detección de pose estable")

    # ── clasificación en juego:  G = f(H, C) ────────────────────────────
    def classify(self, landmarks_flat: np.ndarray) -> str | None:
        """Compara la mano actual contra las referencias calibradas.

        Devuelve la NOTA más cercana (o None si ninguna supera el umbral).
        """
        raise NotImplementedError("Fase 4: vecino más cercano sobre referencias")

    # ── persistencia ────────────────────────────────────────────────────
    def path(self) -> Path:
        return config.CALIBRATION_DIR / f"{self.user_id}.json"

    def load(self, fallback_to_pentagrama: bool = True) -> CalibrationProfile:
        """Carga la calibración del usuario; si no existe, usa la de referencia."""
        raise NotImplementedError("Fase 4: cargar JSON de calibración")

    def save(self) -> None:
        """Persiste `self.profile` en data/calibration/<user_id>.json."""
        raise NotImplementedError("Fase 4: guardar JSON de calibración")
