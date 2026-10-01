"""Motor musical: convierte gestos en eventos musicales y reproduce melodías.

La separación importante es esta: la visión entrega una seña, el motor musical
la convierte en una nota con su instante, y el evaluador decide si esa nota era
la correcta. Ninguna de las tres cosas conoce a las otras dos.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, QTimer, Signal

from ..core.events import BUS, Event, EventBus
from ..domain.notes import NOTE_CODES, SILENCE, frequency, solfa
from .audio import AudioEngine


@dataclass
class NoteEvent:
    note: str
    at: float = field(default_factory=time.time)
    confidence: float = 1.0
    source: str = "gesto"          # gesto | teclado | reproduccion

    @property
    def solfa(self) -> str:
        return solfa(self.note)

    @property
    def frequency(self) -> float:
        return frequency(self.note)


class MusicEngine(QObject):
    """Emite notas, reproduce secuencias de referencia y marca el pulso."""

    notePlayed = Signal(object)        # NoteEvent
    beat = Signal(int)                 # número de pulso dentro del compás
    playbackFinished = Signal()

    def __init__(self, audio: AudioEngine, bus: EventBus | None = None,
                 parent=None) -> None:
        super().__init__(parent)
        self.audio = audio
        self.bus = bus or BUS
        self.history: list[NoteEvent] = []

        self._playback = QTimer(self)
        self._playback.setSingleShot(True)
        self._playback.timeout.connect(self._advance_playback)
        self._queue: list[str] = []
        self._queue_i = 0
        self._queue_gap_ms = 500

        self._metronome = QTimer(self)
        self._metronome.timeout.connect(self._on_beat)
        self._beat_i = 0
        self._beats_per_bar = 4
        self._audible_metronome = True

    # ------------------------------------------------------------- entrada
    def trigger(self, note: str, confidence: float = 1.0,
                source: str = "gesto") -> NoteEvent | None:
        """Una seña reconocida se convierte en una nota que suena y se anuncia."""
        if note not in NOTE_CODES:
            return None
        ev = NoteEvent(note=note, confidence=confidence, source=source)
        self.history.append(ev)
        self.audio.play_note(note)
        self.notePlayed.emit(ev)
        self.bus.publish(Event.NOTE_PLAYED, note=note, confidence=confidence,
                         source=source, at=ev.at)
        return ev

    def clear_history(self) -> None:
        self.history.clear()

    # -------------------------------------------------------- reproducción
    def play_sequence(self, notes: list[str], bpm: int = 72,
                      gap_factor: float = 1.0) -> None:
        """Toca una melodía para que el niño la escuche antes de imitarla.

        Un silencio (SILENCE) se conserva en la cola: no suena nada, pero el
        tiempo de espera sigue corriendo, así la pausa se escucha como tal."""
        self.stop_playback()
        self._queue = [n for n in notes if n in NOTE_CODES or n == SILENCE]
        self._queue_i = 0
        self._queue_gap_ms = int((60_000 / max(30, bpm)) * gap_factor)
        if self._queue:
            self._advance_playback()

    def _advance_playback(self) -> None:
        if self._queue_i >= len(self._queue):
            self._queue = []
            self.playbackFinished.emit()
            return
        note = self._queue[self._queue_i]
        self._queue_i += 1
        if note == SILENCE:
            self._playback.start(self._queue_gap_ms)
            return
        self.audio.play_note(note, gain=0.9)
        ev = NoteEvent(note=note, source="reproduccion")
        self.notePlayed.emit(ev)
        self._playback.start(self._queue_gap_ms)

    def stop_playback(self) -> None:
        self._playback.stop()
        self._queue = []
        self._queue_i = 0

    @property
    def is_playing(self) -> bool:
        return bool(self._queue)

    # ------------------------------------------------------------- metrónomo
    def start_metronome(self, bpm: int, beats_per_bar: int = 4,
                        audible: bool = True) -> None:
        self._beat_i = 0
        self._beats_per_bar = max(1, beats_per_bar)
        self._audible_metronome = audible
        self._metronome.start(int(60_000 / max(30, bpm)))

    def stop_metronome(self) -> None:
        self._metronome.stop()

    def _on_beat(self) -> None:
        strong = (self._beat_i % self._beats_per_bar) == 0
        if self._audible_metronome:
            self.audio.tick(strong)
        self.beat.emit(self._beat_i % self._beats_per_bar)
        self._beat_i += 1
