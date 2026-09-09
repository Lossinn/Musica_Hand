"""Lógica y dinámica del juego (Pygame).

Dinámicas soportadas (§5): tutorial, uso libre, notas rítmicas, juego de reacción.
Evalúa la respuesta del niño y produce un `ActivityResult` que alimenta el perfil.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from . import config


@dataclass
class EventoObjetivo:
    """Un evento esperado en la secuencia de una actividad."""

    nota: str | None                 # None => silencio (mano quieta)
    figura: str = "negra"            # nombre de curriculum.Figura
    inicio_pulso: float = 0.0        # cuándo debe ocurrir, en pulsos
    en_pentagrama: bool = False      # se muestra como nota (True) o burbuja de color (False)


@dataclass
class Activity:
    """Actividad que se le presenta al niño en un periodo `t`.

    Se construye desde `adaptive.adapter.ParametrosActividad` (ver `desde_parametros`).
    """

    nota_objetivo: str
    dinamica: str = "tutorial"
    dificultad: int = 1
    secuencia: list[EventoObjetivo] = field(default_factory=list)
    bpm: int = 60
    compas: str = "4/4"
    tol_ms: int = 250               # ventana de acierto de tiempo
    ayudas: int = 3                 # nº de apoyos visuales
    duracion_s: float = 10.0
    etapa_id: int = 0
    params: object | None = None    # ParametrosActividad de origen (trazabilidad)

    @classmethod
    def desde_parametros(cls, params, secuencia: list[EventoObjetivo]) -> "Activity":
        """Traduce un `ParametrosActividad` + secuencia generada en una Activity."""
        raise NotImplementedError("Fase 1: construir Activity desde ParametrosActividad")


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
    # ── ritmo ──────────────────────────────────────────────────────────
    figura: str = "negra"
    desfase_ms: float = 0.0         # + tarde / - pronto respecto al pulso
    timing_ok: bool = True          # |desfase_ms| <= tol_ms de la actividad
    # ── contexto ───────────────────────────────────────────────────────
    etapa_id: int = 0
    timestamp: float = field(default_factory=time.time)

    def es_acierto_pleno(self) -> bool:
        """Nota correcta Y a tiempo — lo que cuenta para avanzar de etapa."""
        return self.correcto and self.timing_ok


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

    # ── generación de secuencias ─────────────────────────────────────────
    def generar_secuencia(self, params) -> list[EventoObjetivo]:
        """Crea la secuencia de eventos de una actividad a partir de un
        `adaptive.adapter.ParametrosActividad`: elige notas (respetando
        `p_salto`), figuras (respetando `densidad`) y marca cuáles van en
        pentagrama (`p_lectura`). No sale de `params.notas` / `params.figuras`."""
        raise NotImplementedError("Fase 1: generador de secuencias parametrizado")

    # ── lógica de actividad ──────────────────────────────────────────────
    def evaluate(self, gesture: str | None, t: float | None = None) -> ActivityResult | None:
        """Compara el gesto/nota detectado con el evento objetivo actual y su
        momento esperado (`t` = instante del gesto). Rellena `desfase_ms` y
        `timing_ok` con `self.current_activity.tol_ms`.

        Devuelve un ActivityResult cuando la actividad concluye; None si sigue.
        """
        raise NotImplementedError("Fase 1-2: evaluación de nota + tiempo")

    def next_activity(self, activity: Activity) -> None:
        """Carga la siguiente actividad (construida por el sistema adaptativo)."""
        raise NotImplementedError

    def feedback(self, result: ActivityResult) -> None:
        """Retroalimentación audiovisual al niño (acierto/error/ánimo).
        `result.timing_ok=False` con `correcto=True` -> feedback de ritmo."""
        raise NotImplementedError
