"""Estabilización temporal del reconocimiento.

Un clasificador que trabaja fotograma a fotograma produce una nota nueva cada
40 milisegundos. Aquí se exige que una misma lectura se sostenga durante una
fracción de la ventana antes de confirmarla, y tras confirmarla se impone un
periodo refractario para que una seña mantenida no se repita sin control.

Por defecto la ventana es de un solo fotograma (`window=1`): la nota se
confirma en cuanto el clasificador la reconoce, sin ninguna espera ni "barra
de aceptación" que llenar — el descriptor y el margen de confianza (ver
`vision.descriptor` y `VisionSettings.confidence_threshold`/`margin_threshold`)
ya filtran la enorme mayoría de posturas intermedias por sí solos (8 % de
falsos positivos en transiciones, frente al 100 % del método de la versión 1;
ver `tests/test_vision.py`). Una familia que necesite más margen para un niño
en particular puede subir `window_frames` en Ajustes ("Tiempo de sostener la
seña"): con una ventana más ancha, se vuelve a exigir que la lectura se
sostenga varios fotogramas, como en versiones anteriores de la aplicación.

Con la ventana en un solo fotograma, el mecanismo de "soltar" (`release_frames`,
más abajo) pasa a ser el único filtro contra que una misma nota sostenida
suene dos veces: como ya no hay una votación de varios fotogramas que absorba
un parpadeo del rastreo de la mano (MediaPipe pierde el contorno un fotograma
o dos incluso con la mano perfectamente quieta), un `release_frames` bajo
interpretaba ese parpadeo como si el niño hubiera deshecho la seña, y la
siguiente lectura —la misma nota, sin que el niño hiciera nada— volvía a
sonar. Por eso `release_frames` viene en 6 fotogramas (no en 2): ese parpadeo
típico ya no alcanza para soltar la nota, pero un niño que de verdad baja la
mano o cambia de seña sigue soltándola en bien menos de un segundo."""

from __future__ import annotations

import time
from collections import Counter, deque
from dataclasses import dataclass


@dataclass
class Confirmation:
    note: str
    confidence: float
    at: float
    held_frames: int


class GestureStabilizer:
    def __init__(self, window: int = 1, agreement: float = 0.62,
                 confidence_threshold: float = 0.55,
                 refractory_s: float = 0.45, release_frames: int = 6) -> None:
        self.window = max(1, window)
        self.agreement = agreement
        self.confidence_threshold = confidence_threshold
        self.refractory_s = refractory_s
        self.release_frames = max(1, release_frames)
        self._buffer: deque[tuple[str | None, float]] = deque(maxlen=self.window)
        self._last_confirmed: str | None = None
        self._last_at: float = float("-inf")
        self._release_count: int = 0
        self._released: bool = True

    # --------------------------------------------------------------- estado
    def reset(self) -> None:
        self._buffer.clear()
        self._last_confirmed = None
        self._last_at = float("-inf")
        self._release_count = 0
        self._released = True

    @property
    def current(self) -> tuple[str | None, float]:
        """Lectura provisional: la más votada de la ventana, sin confirmar."""
        labels = [b for b, _ in self._buffer if b]
        if not labels:
            return None, 0.0
        label, votes = Counter(labels).most_common(1)[0]
        confs = [c for b, c in self._buffer if b == label]
        return label, sum(confs) / len(confs)

    @property
    def progress(self) -> float:
        """Cuánto le falta a la lectura actual para confirmarse, de 0 a 1.
        La interfaz lo usa para dibujar el anillo que se va llenando."""
        label, _ = self.current
        if not label:
            return 0.0
        votes = sum(1 for b, _ in self._buffer if b == label)
        needed = max(1, int(round(self.agreement * self.window)))
        return min(1.0, votes / needed)

    # ---------------------------------------------------------------- ciclo
    def push(self, note: str | None, confidence: float,
             now: float | None = None) -> Confirmation | None:
        """Registra la lectura de un fotograma y devuelve la confirmación si
        corresponde."""
        now = now if now is not None else time.time()
        self._buffer.append((note, float(confidence)))

        # "Soltar" es un suceso, no un contador: en cuanto pasan suficientes
        # fotogramas seguidos cuya lectura ya no es la última nota confirmada,
        # queda registrado que el niño deshizo la seña. Es lo que separa
        # mantener la mano quieta de volver a hacer la misma seña a propósito.
        if self._last_confirmed is not None and not self._released:
            if note != self._last_confirmed:
                self._release_count += 1
                if self._release_count >= self.release_frames:
                    self._released = True
            else:
                self._release_count = 0

        label, mean_conf = self.current
        votes = sum(1 for b, _ in self._buffer if b == label) if label else 0
        needed = max(1, int(round(self.agreement * self.window)))

        if not (label and votes >= needed
                and mean_conf >= self.confidence_threshold):
            return None

        # Periodo refractario: dos confirmaciones no pueden ir demasiado juntas.
        if now - self._last_at < self.refractory_s:
            return None

        # Repetir la misma nota exige haberla soltado antes.
        if label == self._last_confirmed and not self._released:
            return None

        self._last_confirmed = label
        self._last_at = now
        self._release_count = 0
        self._released = False
        self._buffer.clear()
        return Confirmation(note=label, confidence=float(mean_conf),
                            at=now, held_frames=votes)
