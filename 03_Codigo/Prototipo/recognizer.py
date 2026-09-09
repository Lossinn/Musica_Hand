"""Reconocimiento de gestos → nota musical (Fase 3). IMPLEMENTADO.

Heredado de la versión anterior (MusicaManos), con la misma estrategia probada:

    landmarks de LAS DOS MANOS  ->  vector 126 (2 · 21 · 3), ordenado por mano
                                ->  similitud coseno contra plantillas calibradas
                                ->  nota de la plantilla más parecida (si supera el umbral)

Separación (§40): el reconocedor **no decide qué enseñar**. Solo responde
"¿qué seña hizo el niño?".

Formato de entrada `hands_data` (lo produce `vision.HandVision.detect`):
    [
      {"landmarks": [[x,y,z], ... 21], "hand_label": "Left"},
      {"landmarks": [[x,y,z], ... 21], "hand_label": "Right"},
    ]
Los landmarks vienen ya centrados en la muñeca (wrist-relative).
"""
from __future__ import annotations

import numpy as np

from . import config


def hands_to_vector(hands_data: list[dict]) -> np.ndarray:
    """Concatena los landmarks de ambas manos en un vector plano.

    Ordena por `hand_label` para que "Left" vaya siempre antes que "Right"
    (así el vector en vivo y la plantilla son comparables). Devuelve un array
    vacío si faltan datos.
    """
    if not hands_data:
        return np.empty(0)
    vector: list[float] = []
    for hand in sorted(hands_data, key=lambda h: h.get("hand_label", "")):
        for lm in hand.get("landmarks", []):
            vector.extend(lm)
    return np.asarray(vector, dtype=float)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Coseno del ángulo entre dos vectores. -1.0 si alguno es nulo o de
    distinta forma."""
    if a.shape != b.shape or a.size == 0:
        return -1.0
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return -1.0
    return float(np.dot(a, b) / (na * nb))


class GestureRecognizer:
    """Clasifica una pose de dos manos en una de las notas de `config.NOTAS`.

    Uso:
        recognizer = GestureRecognizer(calibrator)
        nota = recognizer.recognize(hands_data)   # "SOL3" | None
    """

    def __init__(self, calibrator, threshold: float | None = None) -> None:
        self.calibrator = calibrator
        self.threshold = (
            config.GESTURE_SIMILARITY_THRESHOLD if threshold is None else threshold
        )

    def features(self, hands_data: list[dict]) -> np.ndarray:
        """Vector 126 de la pose en vivo."""
        return hands_to_vector(hands_data)

    def recognize(self, hands_data: list[dict]) -> str | None:
        """Devuelve la NOTA reconocida (config.NOTAS) o None.

        None si: hay menos de dos manos, no hay plantillas calibradas, o la
        mejor similitud no alcanza el umbral.
        """
        if not hands_data or len(hands_data) < config.HANDS_PER_GESTURE:
            return None

        templates = self.calibrator.templates()  # {nota: np.ndarray(126)}
        if not templates:
            return None

        live = self.features(hands_data)
        if live.size == 0:
            return None

        best_note: str | None = None
        best_sim = -1.0
        for note, template_vec in templates.items():
            sim = cosine_similarity(live, template_vec)
            if sim > best_sim:
                best_sim = sim
                best_note = note

        if best_sim < self.threshold:
            return None
        return best_note

    def scores(self, hands_data: list[dict]) -> dict[str, float]:
        """Similitud contra cada plantilla (para depuración / calibración)."""
        live = self.features(hands_data)
        templates = self.calibrator.templates()
        return {n: cosine_similarity(live, v) for n, v in templates.items()}

    @staticmethod
    def gesture_to_note(gesture: str | None) -> str | None:
        """El gesto ya es el nombre de la nota (identidad). None si no es válido."""
        return gesture if gesture in config.NOTAS else None
