"""Envoltorio de MediaPipe Hands.

Se aísla aquí toda la dependencia de MediaPipe: si mañana se cambia de modelo,
el resto de la aplicación no se entera porque sigue recibiendo la misma lista de
diccionarios con `landmarks` y `hand_label`.
"""

from __future__ import annotations

import logging
import os
import warnings

import numpy as np

# MediaPipe es ruidoso al importarse; se silencia para no ensuciar la consola.
os.environ.setdefault("GLOG_minloglevel", "2")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

log = logging.getLogger(__name__)

CONNECTIONS: tuple[tuple[int, int], ...] = (
    (0, 1), (1, 2), (2, 3), (3, 4),            # pulgar
    (0, 5), (5, 6), (6, 7), (7, 8),            # índice
    (5, 9), (9, 10), (10, 11), (11, 12),       # medio
    (9, 13), (13, 14), (14, 15), (15, 16),     # anular
    (13, 17), (17, 18), (18, 19), (19, 20),    # meñique
    (0, 17),                                    # base de la palma
)


class HandDetector:
    """Detecta hasta dos manos y devuelve sus 21 puntos de referencia.

    Debe construirse dentro del hilo que lo va a usar: el grafo interno de
    MediaPipe no se puede compartir entre hilos.
    """

    def __init__(self, detection_confidence: float = 0.6,
                 tracking_confidence: float = 0.5,
                 max_num_hands: int = 2) -> None:
        import mediapipe as mp  # import diferido: tarda cerca de un segundo

        self._mp = mp
        self._hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=0,        # el modelo ligero basta y va al doble de fps
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def detect(self, frame_rgb: np.ndarray) -> list[dict]:
        """Recibe un fotograma RGB y devuelve una lista con una entrada por mano.

        Las coordenadas son las normalizadas de MediaPipe: x e y en [0, 1]
        respecto al ancho y alto de la imagen, z relativa a la muñeca.
        """
        frame_rgb.flags.writeable = False
        results = self._hands.process(frame_rgb)
        frame_rgb.flags.writeable = True

        out: list[dict] = []
        if not results.multi_hand_landmarks:
            return out

        handedness = results.multi_handedness or []
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            label = "Right"
            score = 1.0
            if i < len(handedness):
                cls = handedness[i].classification[0]
                label = cls.label
                score = float(cls.score)
            pts = [[float(lm.x), float(lm.y), float(lm.z)]
                   for lm in hand_landmarks.landmark]
            out.append({"landmarks": pts, "hand_label": label,
                        "handedness_score": score})
        return out

    def close(self) -> None:
        try:
            self._hands.close()
        except Exception:  # pragma: no cover
            pass

    def __enter__(self) -> "HandDetector":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
