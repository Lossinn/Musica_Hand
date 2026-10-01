"""Captura de vídeo y detección en un hilo aparte.

La interfaz nunca se bloquea esperando a la cámara: el hilo trabajador captura,
detecta y emite señales de Qt, que Qt entrega en el hilo gráfico.
"""

from __future__ import annotations

import logging
import time

import numpy as np
from PySide6.QtCore import QThread, Signal

from ..core.config import VisionSettings

log = logging.getLogger(__name__)


class CameraWorker(QThread):
    """Hilo de captura. Emite el fotograma ya volteado para mostrar y, por
    separado, los puntos de las manos en coordenadas de la imagen original."""

    frameReady = Signal(object, object)   # (np.ndarray RGB mostrado, list[dict] manos)
    started_ok = Signal()
    failed = Signal(str)
    fpsChanged = Signal(float)

    def __init__(self, settings: VisionSettings, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self._running = False
        self._paused = False
        self._detect_every = 1          # se ajusta solo si el equipo va justo
        self._source = None             # fuente alternativa para pruebas

    # ------------------------------------------------------------- control
    def stop(self) -> None:
        self._running = False
        self.wait(2500)

    def pause(self, value: bool = True) -> None:
        self._paused = value

    def set_source(self, source) -> None:
        """Inyecta una fuente simulada: cualquier objeto con `read() -> frame`."""
        self._source = source

    # ---------------------------------------------------------------- ciclo
    def run(self) -> None:  # noqa: C901
        import cv2

        cap = None
        detector = None
        try:
            from .detector import HandDetector
            detector = HandDetector(
                detection_confidence=self.settings.detection_confidence,
                tracking_confidence=self.settings.tracking_confidence,
                max_num_hands=self.settings.max_num_hands,
            )
        except Exception as exc:  # pragma: no cover
            self.failed.emit(f"No se pudo iniciar el detector de manos: {exc}")
            return

        if self._source is None:
            cap = self._open_capture(cv2)
            if cap is None:
                detector.close()
                self.failed.emit(
                    "No se encontró ninguna cámara disponible. Revisa que otra "
                    "aplicación no la esté usando y que el permiso de cámara "
                    "esté concedido.")
                return

        self._running = True
        self.started_ok.emit()

        target_dt = 1.0 / max(1, self.settings.target_fps)
        frame_i = 0
        last_hands: list[dict] = []
        fps_mark = time.time()
        fps_count = 0

        try:
            while self._running:
                t0 = time.time()
                if self._paused:
                    self.msleep(60)
                    continue

                if self._source is not None:
                    frame_bgr = self._source.read()
                    ok = frame_bgr is not None
                else:
                    ok, frame_bgr = cap.read()  # type: ignore[union-attr]
                if not ok:
                    self.msleep(20)
                    continue

                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

                # La detección corre sobre una copia reducida: los puntos vienen
                # normalizados, así que sirven igual para la imagen grande.
                frame_i += 1
                if frame_i % self._detect_every == 0:
                    small = cv2.resize(frame_rgb, (480, 270),
                                       interpolation=cv2.INTER_AREA)
                    last_hands = detector.detect(np.ascontiguousarray(small))

                shown = frame_rgb
                if self.settings.mirror:
                    shown = np.ascontiguousarray(frame_rgb[:, ::-1])

                self.frameReady.emit(shown, last_hands)

                fps_count += 1
                if time.time() - fps_mark >= 1.0:
                    fps = fps_count / (time.time() - fps_mark)
                    self.fpsChanged.emit(fps)
                    # Si el equipo no alcanza, se detecta un fotograma de cada dos.
                    self._detect_every = 2 if fps < 14 else 1
                    fps_mark, fps_count = time.time(), 0

                elapsed = time.time() - t0
                if elapsed < target_dt:
                    self.msleep(int((target_dt - elapsed) * 1000))
        except Exception as exc:  # pragma: no cover
            log.exception("fallo en el hilo de cámara")
            self.failed.emit(str(exc))
        finally:
            if cap is not None:
                cap.release()
            detector.close()

    # ------------------------------------------------------------- apertura
    def _open_capture(self, cv2):
        """Prueba el índice configurado y, si falla, los primeros puertos."""
        candidates = [self.settings.camera_index] + [
            i for i in range(4) if i != self.settings.camera_index]
        for idx in candidates:
            try:
                cap = cv2.VideoCapture(idx)
            except Exception:
                continue
            if cap is not None and cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings.frame_width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings.frame_height)
                cap.set(cv2.CAP_PROP_FPS, self.settings.target_fps)
                ok, _ = cap.read()
                if ok:
                    self.settings.camera_index = idx
                    return cap
                cap.release()
        return None


class SyntheticSource:
    """Fuente de vídeo falsa para probar la aplicación sin cámara.

    Devuelve un degradado animado; no produce manos, de modo que sirve para
    verificar la interfaz, no el reconocimiento.
    """

    def __init__(self, width: int = 640, height: int = 360) -> None:
        self.width, self.height = width, height
        self._t = 0

    def read(self):
        self._t += 1
        y = np.linspace(0, 255, self.height, dtype=np.uint8)[:, None]
        x = np.linspace(0, 255, self.width, dtype=np.uint8)[None, :]
        b = np.full((self.height, self.width), (self._t * 3) % 255, np.uint8)
        return np.dstack([b, np.broadcast_to(y, (self.height, self.width)),
                          np.broadcast_to(x, (self.height, self.width))])
