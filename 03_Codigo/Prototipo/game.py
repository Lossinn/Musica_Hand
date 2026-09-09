"""Lógica y dinámica del juego (Pygame).

Dinámicas soportadas (§5): tutorial, uso libre, notas rítmicas, juego de reacción.
Evalúa la respuesta del niño y produce un `ActivityResult` que alimenta el perfil.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from . import config


@dataclass
class Activity:
    """Actividad que se le presenta al niño en un periodo `t`."""

    nota_objetivo: str
    dinamica: str = "tutorial"
    dificultad: int = 1
    secuencia: list[str] = field(default_factory=list)   # para notas rítmicas
    duracion_s: float = 10.0


@dataclass
class ActivityResult:
    """Resultado observado `O_t` de una actividad (§31)."""

    nota_esperada: str
    nota_detectada: str | None
    correcto: bool
    tiempo_respuesta: float
    intentos: int = 1
    errores: int = 0
    dificultad: int = 1
    dinamica: str = "tutorial"
    timestamp: float = field(default_factory=time.time)


class MusicGame:
    """Bucle y estado del juego.

    Uso previsto (ver main.py):

        game = MusicGame()
        while game.running:
            ...
            result = game.evaluate(gesture)
            game.next_activity(activity)
    """

    def __init__(self) -> None:
        self.running: bool = False
        self.current_activity: Activity | None = None
        self._screen = None                 # pygame.Surface
        self._clock = None                  # pygame.time.Clock
        self._activity_started_at: float = 0.0

    # ── ciclo de vida ────────────────────────────────────────────────────
    def start(self) -> None:
        """Inicializa Pygame, ventana y reloj; deja running = True."""
        raise NotImplementedError("Fase 1: init de Pygame")

    def stop(self) -> None:
        raise NotImplementedError

    def handle_events(self) -> None:
        """Procesa eventos de Pygame (cierre, teclas)."""
        raise NotImplementedError

    def render(self, frame=None, hand=None) -> None:
        """Dibuja pentagrama, nota objetivo, feedback y (opcional) la cámara."""
        raise NotImplementedError("Fase 1: render del pentagrama y notas")

    def tick(self) -> None:
        """Avanza el reloj al FPS objetivo."""
        raise NotImplementedError

    # ── lógica de actividad ──────────────────────────────────────────────
    def evaluate(self, gesture: str | None) -> ActivityResult | None:
        """Compara el gesto/nota detectado con la nota objetivo actual.

        Devuelve un ActivityResult cuando la actividad concluye; None si sigue.
        """
        raise NotImplementedError("Fase 1-2: evaluación de la respuesta")

    def next_activity(self, activity: Activity) -> None:
        """Carga la siguiente actividad (elegida por el sistema adaptativo)."""
        raise NotImplementedError

    def feedback(self, result: ActivityResult) -> None:
        """Retroalimentación audiovisual al niño (acierto/error/ánimo)."""
        raise NotImplementedError
