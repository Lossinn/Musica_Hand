"""Capa de visión computacional (Fase 2). IMPLEMENTADO (cámara real).

Responsabilidad única: **¿qué hizo el niño?**
Captura de cámara (OpenCV) + detección de manos y landmarks (MediaPipe Hands).

No decide qué enseñar ni evalúa: entrega `hands_data` (una entrada por mano,
landmarks centrados en la muñeca), listo para `recognizer` / `calibration`.

    vision = HandVision(camera_index=0)
    with vision:
        hands_data, frame = vision.read()
        nota = vision.recognize(hands_data, calibrator)

`cv2` y `mediapipe` se importan de forma perezosa: el módulo se puede importar
(y testear) sin cámara ni esas dependencias instaladas.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import config
from .recognizer import GestureRecognizer

try:  # dependencias de runtime, no de import
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

try:
    import mediapipe as mp
except ImportError:  # pragma: no cover
    mp = None


@dataclass
class HandObservation:
    """Una mano detectada en un frame (landmarks ya centrados en la muñeca)."""

    landmarks: np.ndarray          # shape (21, 3)
    hand_label: str = "unknown"    # "Left" / "Right"
    score: float = 0.0

    @property
    def flat(self) -> np.ndarray:
        return self.landmarks.reshape(-1)

    def as_dict(self) -> dict:
        return {"landmarks": self.landmarks.tolist(), "hand_label": self.hand_label}


class VisionUnavailable(RuntimeError):
    """No hay cámara o faltan cv2/mediapipe."""


def _has_legacy_solutions() -> bool:
    return mp is not None and hasattr(mp, "solutions") and hasattr(mp.solutions, "hands")


class MediaPipeHandDetector:
    """Detecta hasta 2 manos y normaliza los landmarks restando la muñeca.

    Soporta las dos APIs de MediaPipe:
      · **legacy** `mp.solutions.hands` (0.10.x) — preferida, es la que usó la
        versión anterior (MusicaManos);
      · **Tasks** `mp.tasks.vision.HandLandmarker` (>= 1.0) — necesita el modelo
        `models/gesture/hand_landmarker.task` (ver tools/descargar_modelo.py).

    En ambos casos `detect()` devuelve el mismo formato `hands_data`.
    """

    def __init__(
        self,
        detection_conf: float = config.MIN_DETECTION_CONFIDENCE,
        tracking_conf: float = config.MIN_TRACKING_CONFIDENCE,
        max_hands: int = config.MAX_HANDS,
    ) -> None:
        if mp is None:
            raise VisionUnavailable("mediapipe no está instalado (pip install -r requirements.txt)")
        self._api = "legacy" if _has_legacy_solutions() else "tasks"
        self._draw = None
        if self._api == "legacy":
            self._mp_hands = mp.solutions.hands
            self._draw = mp.solutions.drawing_utils
            self._hands = self._mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=max_hands,
                min_detection_confidence=detection_conf,
                min_tracking_confidence=tracking_conf,
            )
        else:
            self._hands = _build_tasks_landmarker(max_hands, detection_conf, tracking_conf)

    # ── API pública ────────────────────────────────────────────────────
    def detect(self, frame_rgb: np.ndarray, draw: bool = True) -> tuple[list[dict], np.ndarray]:
        if self._api == "legacy":
            return self._detect_legacy(frame_rgb, draw)
        return self._detect_tasks(frame_rgb)

    def close(self) -> None:
        try:
            self._hands.close()
        except Exception:  # noqa: BLE001
            pass

    # ── legacy (mp.solutions.hands) ────────────────────────────────────
    def _detect_legacy(self, frame_rgb, draw):
        results = self._hands.process(frame_rgb)
        hands_data: list[dict] = []
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                label = handedness.classification[0].label
                score = float(handedness.classification[0].score)
                wrist = hand_landmarks.landmark[self._mp_hands.HandLandmark.WRIST]
                hands_data.append({
                    "landmarks": [
                        [lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z]
                        for lm in hand_landmarks.landmark
                    ],
                    "hand_label": label,
                    "score": score,
                })
                if draw and self._draw is not None:
                    self._draw.draw_landmarks(
                        frame_rgb, hand_landmarks, self._mp_hands.HAND_CONNECTIONS
                    )
        return hands_data, frame_rgb

    # ── tasks (mp.tasks.vision.HandLandmarker) ─────────────────────────
    def _detect_tasks(self, frame_rgb):
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(frame_rgb))
        result = self._hands.detect(image)
        hands_data: list[dict] = []
        for lms, handedness in zip(result.hand_landmarks, result.handedness):
            label = handedness[0].category_name           # "Left" / "Right"
            score = float(handedness[0].score)
            wrist = lms[0]
            hands_data.append({
                "landmarks": [[lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z] for lm in lms],
                "hand_label": label,
                "score": score,
            })
        return hands_data, frame_rgb


def _build_tasks_landmarker(max_hands: int, det_conf: float, track_conf: float):
    model = config.MODELS_DIR / "gesture" / "hand_landmarker.task"
    if not model.exists():
        raise VisionUnavailable(
            "MediaPipe >= 1.0 detectado (API Tasks) pero falta el modelo "
            f"{model}. Descárgalo con:  python -m Prototipo.tools.descargar_modelo\n"
            "O instala la API clásica:  pip install 'mediapipe>=0.10.14,<0.11'"
        )
    from mediapipe.tasks import python as _tpy
    from mediapipe.tasks.python import vision as _tvision

    opts = _tvision.HandLandmarkerOptions(
        base_options=_tpy.BaseOptions(model_asset_path=str(model)),
        running_mode=_tvision.RunningMode.IMAGE,
        num_hands=max_hands,
        min_hand_detection_confidence=det_conf,
        min_tracking_confidence=track_conf,
    )
    return _tvision.HandLandmarker.create_from_options(opts)


class HandVision:
    """Cámara + detector. `hands_data` es la moneda de cambio con el resto."""

    def __init__(
        self,
        camera_index: int = config.CAMERA_INDEX,
        max_hands: int = config.MAX_HANDS,
        draw_landmarks: bool = True,
    ) -> None:
        self.camera_index = camera_index
        self.max_hands = max_hands
        self.draw_landmarks = draw_landmarks
        self._capture = None          # cv2.VideoCapture
        self._detector: MediaPipeHandDetector | None = None
        self.last_hands: list[dict] = []
        self.last_frame: np.ndarray | None = None      # RGB, con landmarks dibujados

    # ── ciclo de vida ────────────────────────────────────────────────────
    def open(self) -> None:
        if cv2 is None:
            raise VisionUnavailable("opencv-python no está instalado")
        self._capture = cv2.VideoCapture(self.camera_index)
        if not self._capture.isOpened():
            self._capture = None
            raise VisionUnavailable(
                f"No se pudo abrir la cámara en el índice {self.camera_index}. "
                f"Prueba otros índices con tools/probar_camara.py."
            )
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self._detector = MediaPipeHandDetector(max_hands=self.max_hands)

    def close(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None
        if self._detector is not None:
            self._detector.close()
            self._detector = None

    def __enter__(self) -> "HandVision":
        self.open()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    @property
    def disponible(self) -> bool:
        return self._capture is not None and self._detector is not None

    # ── pipeline ─────────────────────────────────────────────────────────
    def read(self) -> tuple[list[dict], np.ndarray | None]:
        """Captura un frame, detecta manos y devuelve (hands_data, frame_rgb).

        `hands_data` vacío si no hay manos; `frame` None si la cámara no dio
        frame. Refleja horizontalmente (efecto espejo, natural para el niño).
        """
        if not self.disponible:
            raise VisionUnavailable("HandVision.open() no se ha llamado")
        ok, frame_bgr = self._capture.read()
        if not ok:
            return [], None
        frame_bgr = cv2.flip(frame_bgr, 1)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        hands_data, drawn = self._detector.detect(frame_rgb, self.draw_landmarks)
        self.last_hands, self.last_frame = hands_data, drawn
        return hands_data, drawn

    def recognize(self, hands_data: list[dict], calibrator) -> str | None:
        """Atajo: delega en `GestureRecognizer` con la calibración dada."""
        return GestureRecognizer(calibrator).recognize(hands_data)

    @staticmethod
    def observations(hands_data: list[dict]) -> list[HandObservation]:
        """Convierte `hands_data` en dataclasses tipadas (uso opcional)."""
        return [
            HandObservation(
                landmarks=np.asarray(h["landmarks"], dtype=float),
                hand_label=h.get("hand_label", "unknown"),
                score=float(h.get("score", 0.0)),
            )
            for h in hands_data
        ]
