"""Bus de eventos de la aplicación.

La regla del rediseño es que una pantalla nunca habla directamente con la
cámara ni con el motor musical: publica y escucha eventos. Esto permite probar
el juego sin cámara y cambiar el reconocedor sin tocar la interfaz.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Event(str, Enum):
    # --- visión ---
    CAMERA_STARTED = "camera.started"
    CAMERA_FAILED = "camera.failed"
    CAMERA_STOPPED = "camera.stopped"
    FRAME_READY = "vision.frame_ready"
    HANDS_UPDATED = "vision.hands_updated"
    GESTURE_CANDIDATE = "vision.gesture_candidate"
    GESTURE_CONFIRMED = "vision.gesture_confirmed"

    # --- música ---
    NOTE_PLAYED = "music.note_played"

    # --- ejercicio ---
    EXERCISE_STARTED = "exercise.started"
    STEP_ADVANCED = "exercise.step_advanced"
    ATTEMPT_CORRECT = "exercise.attempt_correct"
    ATTEMPT_WRONG = "exercise.attempt_wrong"
    HINT_SHOWN = "exercise.hint_shown"
    EXERCISE_COMPLETED = "exercise.completed"
    EXERCISE_ABANDONED = "exercise.abandoned"

    # --- progreso ---
    SKILL_UPDATED = "progress.skill_updated"
    LEVEL_UNLOCKED = "progress.level_unlocked"
    REWARD_EARNED = "progress.reward_earned"
    ACHIEVEMENT_UNLOCKED = "progress.achievement_unlocked"

    # --- calibración ---
    CALIBRATION_STEP = "calibration.step"
    CALIBRATION_SAVED = "calibration.saved"

    # --- sesión ---
    PROFILE_SELECTED = "session.profile_selected"
    SESSION_STARTED = "session.started"
    SESSION_ENDED = "session.ended"


@dataclass
class Message:
    event: Event
    payload: dict[str, Any] = field(default_factory=dict)
    at: float = field(default_factory=time.time)

    def get(self, key: str, default: Any = None) -> Any:
        return self.payload.get(key, default)


Handler = Callable[[Message], None]


class EventBus:
    """Publicador/suscriptor mínimo y síncrono.

    Los manejadores se ejecutan en el hilo que publica. Todo lo que provenga de
    la cámara se reenvía al hilo gráfico mediante señales de Qt antes de
    publicarse aquí, de modo que la interfaz nunca se toca desde otro hilo.
    """

    def __init__(self) -> None:
        self._subs: dict[Event, list[Handler]] = defaultdict(list)
        self._any: list[Handler] = []
        self._log: list[Message] = []
        self.keep_log = False

    def subscribe(self, event: Event, handler: Handler) -> Callable[[], None]:
        self._subs[event].append(handler)
        return lambda: self.unsubscribe(event, handler)

    def subscribe_any(self, handler: Handler) -> Callable[[], None]:
        self._any.append(handler)
        return lambda: self._any.remove(handler) if handler in self._any else None

    def unsubscribe(self, event: Event, handler: Handler) -> None:
        if handler in self._subs[event]:
            self._subs[event].remove(handler)

    def publish(self, event: Event, **payload: Any) -> Message:
        msg = Message(event=event, payload=payload)
        if self.keep_log:
            self._log.append(msg)
        for handler in list(self._subs[event]):
            handler(msg)
        for handler in list(self._any):
            handler(msg)
        return msg

    def clear(self) -> None:
        self._subs.clear()
        self._any.clear()
        self._log.clear()

    @property
    def log(self) -> list[Message]:
        return list(self._log)


BUS = EventBus()
