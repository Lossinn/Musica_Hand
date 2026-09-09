"""Capa de visión computacional.

Responsabilidad única: **¿qué hizo el niño?**
Captura de cámara (OpenCV) + detección de mano y landmarks (MediaPipe).

No decide qué enseñar ni evalúa: solo entrega gestos/landmarks.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import config


@dataclass
class HandObservation:
    """Resultado de detectar una mano en un frame."""

    landmarks: np.ndarray          # shape (21, 3) -> (x, y, z) normalizados por MediaPipe
    handedness: str = "unknown"    # "Left" / "Right"
    score: float = 0.0

    @property
    def flat(self) -> np.ndarray:
        """Vector de 63 características (21 * 3)."""
        return self.landmarks.reshape(-1)


class HandVision:
    """Encapsula cámara + MediaPipe Hands.

    Uso previsto (ver main.py):

        vision = HandVision()
        frame = vision.capture()
        hand = vision.detect(frame)
        if hand:
            gesture = vision.recognize(hand, calibrator)
    """

    def __init__(
        self,
        camera_index: int = config.CAMERA_INDEX,
        max_hands: int = config.MAX_HANDS,
    ) -> None:
        self.camera_index = camera_index
        self.max_hands = max_hands
        self._capture = None      # cv2.VideoCapture
        self._hands = None        # mediapipe.solutions.hands.Hands
        self._recognizer = None   # recognizer.GestureRecognizer (inyectado / perezoso)

    # ── ciclo de vida ────────────────────────────────────────────────────
    def open(self) -> None:
        """Inicializa la cámara y el grafo de MediaPipe."""
        raise NotImplementedError("Fase 2: abrir cv2.VideoCapture + mp Hands")

    def close(self) -> None:
        """Libera cámara y recursos de MediaPipe."""
        raise NotImplementedError

    def __enter__(self) -> "HandVision":
        self.open()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ── pipeline ─────────────────────────────────────────────────────────
    def capture(self) -> np.ndarray:
        """Devuelve el frame actual de la cámara (BGR)."""
        raise NotImplementedError("Fase 2: leer un frame")

    def detect(self, frame: np.ndarray) -> HandObservation | None:
        """Detecta una mano en el frame y devuelve sus 21 landmarks.

        Devuelve None si no hay mano.
        """
        raise NotImplementedError("Fase 2: MediaPipe -> HandObservation")

    def recognize(self, hand: HandObservation, calibrator) -> str | None:
        """Atajo: delega en GestureRecognizer usando la calibración dada.

        Devuelve la NOTA identificada (str de config.NOTAS) o None.
        """
        raise NotImplementedError("Fase 3: usar recognizer.GestureRecognizer")

    @staticmethod
    def draw(frame: np.ndarray, hand: HandObservation | None) -> np.ndarray:
        """Dibuja los landmarks sobre el frame (debug/preview)."""
        raise NotImplementedError
