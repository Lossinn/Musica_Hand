"""Reconocimiento de gestos → nota musical.

Cadena (§7):
    landmarks -> normalización -> características -> comparación/clasificación
             -> gesto -> nota

Separación clave (§40): el reconocimiento **no decide qué enseñar**.
Solo responde "¿qué gesto hizo el niño?".
"""
from __future__ import annotations

import numpy as np

from . import config


class GestureRecognizer:
    """Clasifica un conjunto de landmarks en una de las 7 notas.

    Estrategia inicial (Fase 3): comparación contra las referencias calibradas
    (vecino más cercano sobre características relativas).
    Estrategia posible (más adelante): modelo entrenado en models/gesture/.
    """

    def __init__(self, calibrator, threshold: float = 0.15) -> None:
        self.calibrator = calibrator
        self.threshold = threshold

    def features(self, landmarks_flat: np.ndarray) -> np.ndarray:
        """Delega en la normalización del calibrador (características relativas)."""
        return self.calibrator.normalize(landmarks_flat)

    def recognize(self, landmarks_flat: np.ndarray) -> str | None:
        """Devuelve la NOTA reconocida (config.NOTAS) o None."""
        raise NotImplementedError("Fase 3: clasificar características -> nota")

    @staticmethod
    def gesture_to_note(gesture: str) -> str | None:
        """Mapeo gesto -> nota. Por ahora 1:1 (el gesto ya es el nombre de nota)."""
        return gesture if gesture in config.NOTAS else None
