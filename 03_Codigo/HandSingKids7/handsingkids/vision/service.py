"""Servicio de reconocimiento: une cámara, descriptor, clasificador y filtro.

Es la única pieza que la interfaz necesita conocer. Publica en el bus los
eventos de mano detectada, gesto candidato y gesto confirmado; las pantallas se
suscriben a lo que les interese.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal

from ..core.config import Settings
from ..core.events import BUS, Event, EventBus
from .camera import CameraWorker
from .classifier import GestureClassifier, Prediction
from .features import PoseFeatures, pose_features
from .stabilizer import GestureStabilizer
from .templates import TemplateStore, load_or_import

log = logging.getLogger(__name__)


class GestureService(QObject):
    frameReady = Signal(object, object)      # (imagen RGB, manos)
    stateChanged = Signal(str)               # 'inactivo' | 'activo' | 'error'

    def __init__(self, settings: Settings, bus: EventBus | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.bus = bus or BUS
        self.store: TemplateStore | None = None
        self.classifier: GestureClassifier | None = None
        self.stabilizer = self._build_stabilizer()
        self.worker: CameraWorker | None = None
        self.last_prediction: Prediction | None = None
        self.last_pose: PoseFeatures | None = None
        self.last_hands: list[dict] = []
        self.error: str | None = None
        self._enabled = True                 # False durante la calibración
        self._synthetic = False

    # ------------------------------------------------------------- montaje
    def _build_stabilizer(self) -> GestureStabilizer:
        v = self.settings.vision
        return GestureStabilizer(
            window=v.window_frames, agreement=v.agreement_ratio,
            confidence_threshold=v.confidence_threshold,
            refractory_s=v.refractory_seconds, release_frames=v.release_frames)

    def set_profile(self, profile_id: int) -> bool:
        """Carga las plantillas del niño. Devuelve si están completas."""
        self.store = load_or_import(profile_id)
        v = self.settings.vision
        self.classifier = GestureClassifier(
            self.store, confidence_threshold=v.confidence_threshold,
            margin_threshold=v.margin_threshold)
        if self.store.samples:
            self.classifier.calibrate_temperature()
        self.stabilizer = self._build_stabilizer()
        return self.store.is_complete

    def refresh_thresholds(self) -> None:
        v = self.settings.vision
        if self.classifier:
            self.classifier.confidence_threshold = v.confidence_threshold
            self.classifier.margin_threshold = v.margin_threshold
        self.stabilizer = self._build_stabilizer()

    @property
    def calibrated(self) -> bool:
        return bool(self.store and self.store.is_complete)

    @property
    def running(self) -> bool:
        return bool(self.worker and self.worker.isRunning())

    # -------------------------------------------------------------- cámara
    def start(self, synthetic: bool = False) -> None:
        if self.running:
            return
        self.error = None
        self._synthetic = synthetic
        self.worker = CameraWorker(self.settings.vision)
        if synthetic:
            from .camera import SyntheticSource
            self.worker.set_source(SyntheticSource())
        self.worker.frameReady.connect(self._on_frame)
        self.worker.failed.connect(self._on_failed)
        self.worker.started_ok.connect(self._on_started)
        self.worker.start()

    def stop(self) -> None:
        if self.worker:
            self.worker.stop()
            self.worker = None
        self.stabilizer.reset()
        self.bus.publish(Event.CAMERA_STOPPED)
        self.stateChanged.emit("inactivo")

    def pause(self, value: bool = True) -> None:
        if self.worker:
            self.worker.pause(value)

    def set_enabled(self, value: bool) -> None:
        """Con False se siguen viendo las manos pero no se confirman notas."""
        self._enabled = value
        self.stabilizer.reset()

    # -------------------------------------------------------------- señales
    def _on_started(self) -> None:
        self.bus.publish(Event.CAMERA_STARTED,
                         index=self.settings.vision.camera_index)
        self.stateChanged.emit("activo")

    def _on_failed(self, message: str) -> None:
        self.error = message
        self.bus.publish(Event.CAMERA_FAILED, message=message)
        self.stateChanged.emit("error")

    def _on_frame(self, frame, hands: list[dict]) -> None:
        self.last_hands = hands
        self.frameReady.emit(frame, hands)
        self.bus.publish(Event.HANDS_UPDATED, hands=len(hands))

        pose = pose_features(hands) if hands else None
        self.last_pose = pose

        if not self._enabled or self.classifier is None or not self.classifier.ready:
            return

        v = self.settings.vision
        if v.require_two_hands and (pose is None or pose.hands < 2):
            self.stabilizer.push(None, 0.0)
            self.last_prediction = None
            return

        pred = self.classifier.classify(pose)
        self.last_prediction = pred
        self.bus.publish(Event.GESTURE_CANDIDATE, note=pred.note,
                         confidence=pred.confidence, margin=pred.margin,
                         progress=self.stabilizer.progress)

        confirmation = self.stabilizer.push(pred.note, pred.confidence)
        if confirmation:
            self.bus.publish(Event.GESTURE_CONFIRMED,
                             note=confirmation.note,
                             confidence=confirmation.confidence,
                             at=confirmation.at)

    # ---------------------------------------------------------- calibración
    def capture_sample(self, note: str) -> bool:
        """Guarda la postura actual como muestra de una nota."""
        if self.store is None or not self.last_hands:
            return False
        v = self.settings.vision
        if v.require_two_hands and len(self.last_hands) < 2:
            return False
        ok = self.store.add_sample(note, self.last_hands)
        if ok:
            self.bus.publish(Event.CALIBRATION_STEP, note=note,
                             samples=self.store.count(note))
        return ok

    def finish_calibration(self) -> dict:
        """Guarda las plantillas y devuelve un informe de separación entre señas."""
        if self.store is None:
            return {}
        self.store.save()
        if self.classifier:
            self.classifier.calibrate_temperature()
        pairs = self.store.separation()
        report = {
            "notas": len(self.store.notes),
            "completa": self.store.is_complete,
            "parecidas": pairs[:3],
            "separacion_minima": pairs[0][2] if pairs else 0.0,
            "temperatura": self.classifier.temperature if self.classifier else 0.0,
        }
        self.bus.publish(Event.CALIBRATION_SAVED, **report)
        return report
