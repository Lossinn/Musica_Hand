"""Ejecución y evaluación de una actividad.

Este objeto es el árbitro de una partida: sabe qué nota toca, recibe las señas
confirmadas, decide si el intento fue correcto, mide el tiempo de reacción y, al
terminar, produce el resultado. No dibuja nada ni habla con la cámara.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, QTimer, Signal

from ..core.events import BUS, Event, EventBus
from ..domain.entities import Activity, ActivityResult, Attempt, PlayMode

# Tramos de calidad según el tiempo de reacción, en milisegundos.
TIER_PERFECT_MS = 1400
TIER_GOOD_MS = 2600
TIER_POINTS = {"perfecto": 100, "bien": 70, "vale": 50}

# Intentos fallidos antes de mostrar la ayuda visual.
HINT_AFTER_FAILS = 2
# Intentos fallidos antes de dar el paso por perdido y avanzar.
GIVE_UP_AFTER = 4


@dataclass
class StepState:
    index: int
    expected: str
    started_at: float = field(default_factory=time.time)
    fails: int = 0
    hint_shown: bool = False


class ActivityRunner(QObject):
    """Máquina de estados de una actividad."""

    stepChanged = Signal(object)          # StepState
    feedback = Signal(str, str)           # (tipo, mensaje) tipo: acierto|casi|ayuda
    finished = Signal(object)             # ActivityResult
    scoreChanged = Signal(int, int)       # (puntaje, combo)

    def __init__(self, activity: Activity, profile_id: int,
                 age_band: str = "medianos", bus: EventBus | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self.activity = activity
        self.profile_id = profile_id
        self.age_band = age_band
        self.bus = bus or BUS

        self.sequence = list(activity.sequence) * max(1, activity.repetitions)
        self.step: StepState | None = None
        self.attempts: list[Attempt] = []
        self.started_at = 0.0
        self.finished_at = 0.0

        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.steps_correct = 0
        self.confidences: list[float] = []
        self.intervals: list[float] = []
        self._last_correct_at = 0.0
        self._running = False
        self._accepting = False

        self._timeout = QTimer(self)
        self._timeout.setSingleShot(True)
        self._timeout.timeout.connect(self._on_timeout)

    # ------------------------------------------------------------- estado
    @property
    def total_steps(self) -> int:
        return len(self.sequence)

    @property
    def running(self) -> bool:
        return self._running

    @property
    def progress(self) -> float:
        if not self.sequence or self.step is None:
            return 0.0
        return self.step.index / len(self.sequence)

    @property
    def accuracy(self) -> float:
        if not self.attempts:
            return 0.0
        return 100.0 * self.steps_correct / max(1, self.total_steps)

    def upcoming(self, count: int = 4) -> list[str]:
        if self.step is None:
            return self.sequence[:count]
        return self.sequence[self.step.index:self.step.index + count]

    # -------------------------------------------------------------- ciclo
    def start(self) -> None:
        self.started_at = time.time()
        self._last_correct_at = self.started_at
        self._running = True
        self.bus.publish(Event.EXERCISE_STARTED, activity=self.activity.code,
                         steps=self.total_steps)
        self._enter_step(0)

    def _enter_step(self, index: int) -> None:
        if index >= len(self.sequence):
            self.finish()
            return
        self.step = StepState(index=index, expected=self.sequence[index])
        self._accepting = True
        self.stepChanged.emit(self.step)
        self.bus.publish(Event.STEP_ADVANCED, index=index,
                         expected=self.step.expected,
                         total=self.total_steps)
        # Un paso no puede quedarse esperando para siempre.
        self._timeout.start(max(6000, self.activity.tolerance_ms * 4))

    def _on_timeout(self) -> None:
        if not self._running or self.step is None:
            return
        self.step.fails += 1
        if not self.step.hint_shown and self.step.fails >= HINT_AFTER_FAILS:
            self._show_hint()
        if self.step.fails >= GIVE_UP_AFTER:
            self._register(detected=None, confidence=0.0, correct=False,
                           reaction_ms=int(self.activity.tolerance_ms * 4))
            self.feedback.emit("ayuda", "Vamos a la siguiente 😊")
            self._enter_step(self.step.index + 1)
        else:
            self.feedback.emit("casi", "¿Intentamos otra vez?")
            self.step.started_at = time.time()
            self._timeout.start(max(6000, self.activity.tolerance_ms * 4))

    def _show_hint(self) -> None:
        if self.step is None:
            return
        self.step.hint_shown = True
        self.bus.publish(Event.HINT_SHOWN, note=self.step.expected,
                         index=self.step.index)
        self.feedback.emit("ayuda", "Mira la seña y cópiala")

    # ------------------------------------------------------------- entrada
    def submit(self, note: str, confidence: float = 1.0) -> bool:
        """Registra una seña confirmada. Devuelve si fue correcta."""
        if not self._running or self.step is None or not self._accepting:
            return False
        self._timeout.stop()
        now = time.time()
        reaction_ms = int((now - self.step.started_at) * 1000)
        correct = (note == self.step.expected)

        self._register(detected=note, confidence=confidence, correct=correct,
                       reaction_ms=reaction_ms)

        if correct:
            self._accepting = False
            self.steps_correct += 1
            self.confidences.append(confidence)
            self.intervals.append(now - self._last_correct_at)
            self._last_correct_at = now
            tier = self._tier(reaction_ms)
            self._award(tier)
            self.feedback.emit("acierto", self._praise(tier))
            self.bus.publish(Event.ATTEMPT_CORRECT, note=note,
                             index=self.step.index, tier=tier,
                             reaction_ms=reaction_ms)
            QTimer.singleShot(420, self._advance)
            return True

        self.combo = 0
        self.step.fails += 1
        self.bus.publish(Event.ATTEMPT_WRONG, expected=self.step.expected,
                         detected=note, index=self.step.index)
        if not self.step.hint_shown and self.step.fails >= HINT_AFTER_FAILS:
            self._show_hint()
        else:
            self.feedback.emit("casi", "¡Casi! Prueba otra vez")
        if self.step.fails >= GIVE_UP_AFTER:
            self.feedback.emit("ayuda", "Seguimos con la siguiente 😊")
            self._advance()
            return False
        self.step.started_at = time.time()
        self._timeout.start(max(6000, self.activity.tolerance_ms * 4))
        return False

    def _advance(self) -> None:
        if self._running and self.step is not None:
            self._enter_step(self.step.index + 1)

    def _register(self, *, detected: str | None, confidence: float,
                  correct: bool, reaction_ms: int) -> None:
        assert self.step is not None
        self.attempts.append(Attempt(
            profile_id=self.profile_id, activity_code=self.activity.code,
            step_index=self.step.index, expected=self.step.expected,
            detected=detected, confidence=confidence, correct=correct,
            reaction_ms=reaction_ms, attempt_number=self.step.fails + 1))

    # ----------------------------------------------------------- puntaje
    @staticmethod
    def _tier(reaction_ms: int) -> str:
        if reaction_ms <= TIER_PERFECT_MS:
            return "perfecto"
        if reaction_ms <= TIER_GOOD_MS:
            return "bien"
        return "vale"

    @staticmethod
    def _praise(tier: str) -> str:
        return {"perfecto": "¡Excelente!", "bien": "¡Muy bien!",
                "vale": "¡Lo lograste!"}[tier]

    def _award(self, tier: str) -> None:
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        multiplier = min(1.0 + (self.combo // 5) * 0.25, 3.0)
        self.score += int(TIER_POINTS[tier] * multiplier)
        self.scoreChanged.emit(self.score, self.combo)

    # ------------------------------------------------------------- cierre
    def abandon(self) -> None:
        if not self._running:
            return
        self._running = False
        self._timeout.stop()
        self.bus.publish(Event.EXERCISE_ABANDONED, activity=self.activity.code,
                         steps_done=self.steps_correct)

    def finish(self) -> ActivityResult:
        self._running = False
        self._timeout.stop()
        self.finished_at = time.time()
        result = self.build_result()
        self.bus.publish(Event.EXERCISE_COMPLETED, activity=self.activity.code,
                         accuracy=result.accuracy, stars=result.stars)
        self.finished.emit(result)
        return result

    def rhythm_score(self) -> float:
        """Regularidad respecto al pulso objetivo.

        Para cada intervalo entre notas acertadas se mide cuánto se aparta del
        tiempo del compás, y se normaliza por la tolerancia de la actividad:

            r_i = max(0, 1 - |dt_i - T| / tol)

        En los modos sin exigencia rítmica se devuelve el valor neutro 100.
        """
        if self.activity.mode not in (PlayMode.SPEED, PlayMode.MELODY):
            return 100.0
        if len(self.intervals) < 2:
            return 100.0
        target = 60.0 / max(30, self.activity.tempo_bpm)
        tol = max(0.35, self.activity.tolerance_ms / 1000.0)
        vals = [max(0.0, 1.0 - abs(dt - target) / tol) for dt in self.intervals[1:]]
        return round(100.0 * sum(vals) / len(vals), 1)

    def stars(self, accuracy: float) -> int:
        if accuracy >= 90:
            return 3
        if accuracy >= 70:
            return 2
        return 1

    def build_result(self) -> ActivityResult:
        accuracy = round(100.0 * self.steps_correct / max(1, self.total_steps), 1)
        quality = round(100.0 * (sum(self.confidences) / len(self.confidences)), 1) \
            if self.confidences else 0.0
        return ActivityResult(
            profile_id=self.profile_id, activity_code=self.activity.code,
            accuracy=accuracy, rhythm=self.rhythm_score(),
            gesture_quality=quality, stars=self.stars(accuracy),
            score=self.score, max_combo=self.max_combo,
            duration_s=round((self.finished_at or time.time()) - self.started_at, 1),
            steps_total=self.total_steps, steps_correct=self.steps_correct)

    # --------------------------------------------------- resumen por nota
    def per_note_summary(self) -> dict[str, tuple[int, int, float, list[bool]]]:
        """Por nota: aciertos, intentos, tiempo medio de reacción y la
        secuencia de resultados. Es lo que consume el motor de dominio."""
        out: dict[str, list] = {}
        for a in self.attempts:
            entry = out.setdefault(a.expected, [0, 0, [], []])
            entry[1] += 1
            if a.correct:
                entry[0] += 1
                entry[2].append(a.reaction_ms)
            entry[3].append(a.correct)
        return {note: (v[0], v[1],
                       (sum(v[2]) / len(v[2])) if v[2] else 0.0,
                       v[3])
                for note, v in out.items()}
