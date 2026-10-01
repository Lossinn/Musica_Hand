"""Entidades del dominio. Sin dependencias de Qt, de la base de datos ni de la cámara."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class SkillStatus(str, Enum):
    LOCKED = "bloqueada"
    INTRODUCED = "introducida"
    PRACTICING = "en_practica"
    MASTERED = "dominada"
    CONSOLIDATED = "consolidada"

    @property
    def order(self) -> int:
        return list(SkillStatus).index(self)


class ActivityKind(str, Enum):
    EXERCISE = "ejercicio"      # diseñado pedagógicamente
    GAME = "juego"              # práctica con envoltorio lúdico
    SONG = "cancion"            # pieza musical completa
    ASSESSMENT = "evaluacion"   # mide dominio, sin ayudas
    REVIEW = "repaso"           # repaso espaciado


class PlayMode(str, Enum):
    GUIDED = "guiado"       # muestra la seña que debe hacerse
    MEMORY = "memoria"      # muestra la secuencia y la oculta
    SPEED = "velocidad"     # el tempo aumenta
    MELODY = "melodia"      # interpretar una melodía
    CHALLENGE = "reto"      # sin ayuda visual
    FREE = "libre"          # exploración sin objetivo


@dataclass
class Profile:
    id: int | None
    name: str
    age: int
    avatar: str = "iguana"
    created_at: float = field(default_factory=time.time)
    last_seen_at: float = field(default_factory=time.time)
    stars: int = 0
    coins: int = 0
    streak_days: int = 0
    last_play_date: str = ""
    calibrated: bool = False

    @property
    def age_band(self) -> str:
        if self.age <= 5:
            return "pequeños"
        if self.age <= 8:
            return "medianos"
        return "grandes"


@dataclass
class Skill:
    code: str                 # p.ej. "nota_DO3"
    name: str
    note_code: str | None
    level: int
    difficulty: float         # 0..1
    prerequisites: list[str] = field(default_factory=list)
    order_index: int = 0
    description: str = ""


@dataclass
class SkillState:
    """El estado de una habilidad para un niño concreto: el gemelo digital
    se construye con la colección de estos objetos."""
    profile_id: int
    skill_code: str
    status: SkillStatus = SkillStatus.LOCKED
    mastery: float = 0.0
    precision: float = 0.0
    consistency: float = 0.0
    speed: float = 0.0
    retention: float = 1.0
    attempts: int = 0
    hits: int = 0
    mean_reaction_ms: float = 0.0
    last_practice_at: float = 0.0
    due_at: float = 0.0       # próxima fecha de repaso espaciado
    ease: float = 2.3         # factor de facilidad del repaso espaciado
    interval_days: float = 0.0

    @property
    def raw_accuracy(self) -> float:
        return self.hits / self.attempts if self.attempts else 0.0

    @property
    def is_due(self) -> bool:
        return self.due_at > 0 and time.time() >= self.due_at


@dataclass
class Activity:
    code: str
    kind: ActivityKind
    title: str
    level: int
    difficulty: float                    # 0..1
    skill_codes: list[str]
    sequence: list[str]                  # notas esperadas
    mode: PlayMode = PlayMode.GUIDED
    tempo_bpm: int = 72
    duration_s: int = 60
    hints: bool = True
    repetitions: int = 1
    description: str = ""
    icon: str = "🎵"
    tolerance_ms: int = 2500             # ventana para considerar a tiempo

    @property
    def length(self) -> int:
        return len(self.sequence) * max(1, self.repetitions)


@dataclass
class Attempt:
    profile_id: int
    activity_code: str
    step_index: int
    expected: str
    detected: str | None
    confidence: float
    correct: bool
    reaction_ms: int
    attempt_number: int = 1
    session_id: int | None = None
    at: float = field(default_factory=time.time)
    id: int | None = None


@dataclass
class ActivityResult:
    profile_id: int
    activity_code: str
    accuracy: float           # 0..100
    rhythm: float             # 0..100
    gesture_quality: float    # 0..100, confianza media
    stars: int
    score: int
    max_combo: int
    duration_s: float
    steps_total: int
    steps_correct: int
    session_id: int | None = None
    at: float = field(default_factory=time.time)
    id: int | None = None

    @property
    def summary_line(self) -> str:
        return f"{self.steps_correct}/{self.steps_total} · {self.accuracy:.0f}%"


@dataclass
class LearningSession:
    profile_id: int
    started_at: float = field(default_factory=time.time)
    ended_at: float | None = None
    activities_done: int = 0
    accuracy: float = 0.0
    id: int | None = None

    @property
    def duration_s(self) -> float:
        return (self.ended_at or time.time()) - self.started_at


@dataclass
class Reward:
    profile_id: int
    kind: str          # estrella, insignia, moneda, desbloqueo
    code: str
    label: str
    icon: str = "⭐"
    at: float = field(default_factory=time.time)
    id: int | None = None


@dataclass
class Achievement:
    code: str
    title: str
    description: str
    icon: str = "🏆"
