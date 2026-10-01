"""Capa de persistencia: SQLite local, sin servidor y sin red.

Todo lo que registra la aplicación vive en un único archivo dentro de la carpeta
de datos del usuario. No se guarda ninguna imagen de la cámara: solo los puntos
de referencia de las manos durante la calibración y las métricas de desempeño.
"""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any, Iterable

from ..core.config import db_path

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS profiles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    age             INTEGER NOT NULL,
    avatar          TEXT NOT NULL DEFAULT 'iguana',
    created_at      REAL NOT NULL,
    last_seen_at    REAL NOT NULL,
    stars           INTEGER NOT NULL DEFAULT 0,
    coins           INTEGER NOT NULL DEFAULT 0,
    streak_days     INTEGER NOT NULL DEFAULT 0,
    last_play_date  TEXT NOT NULL DEFAULT '',
    calibrated      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS skills (
    code          TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    note_code     TEXT,
    level         INTEGER NOT NULL,
    difficulty    REAL NOT NULL,
    prerequisites TEXT NOT NULL DEFAULT '[]',
    order_index   INTEGER NOT NULL DEFAULT 0,
    description   TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS skill_state (
    profile_id       INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    skill_code       TEXT NOT NULL REFERENCES skills(code) ON DELETE CASCADE,
    status           TEXT NOT NULL DEFAULT 'bloqueada',
    mastery          REAL NOT NULL DEFAULT 0,
    precision_v      REAL NOT NULL DEFAULT 0,
    consistency      REAL NOT NULL DEFAULT 0,
    speed            REAL NOT NULL DEFAULT 0,
    retention        REAL NOT NULL DEFAULT 1,
    attempts         INTEGER NOT NULL DEFAULT 0,
    hits             INTEGER NOT NULL DEFAULT 0,
    mean_reaction_ms REAL NOT NULL DEFAULT 0,
    last_practice_at REAL NOT NULL DEFAULT 0,
    due_at           REAL NOT NULL DEFAULT 0,
    ease             REAL NOT NULL DEFAULT 2.3,
    interval_days    REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (profile_id, skill_code)
);

CREATE TABLE IF NOT EXISTS activities (
    code         TEXT PRIMARY KEY,
    kind         TEXT NOT NULL,
    title        TEXT NOT NULL,
    level        INTEGER NOT NULL,
    difficulty   REAL NOT NULL,
    skill_codes  TEXT NOT NULL DEFAULT '[]',
    sequence     TEXT NOT NULL DEFAULT '[]',
    mode         TEXT NOT NULL DEFAULT 'guiado',
    tempo_bpm    INTEGER NOT NULL DEFAULT 72,
    duration_s   INTEGER NOT NULL DEFAULT 60,
    hints        INTEGER NOT NULL DEFAULT 1,
    repetitions  INTEGER NOT NULL DEFAULT 1,
    description  TEXT NOT NULL DEFAULT '',
    icon         TEXT NOT NULL DEFAULT '🎵',
    tolerance_ms INTEGER NOT NULL DEFAULT 2500
);

CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id      INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    started_at      REAL NOT NULL,
    ended_at        REAL,
    activities_done INTEGER NOT NULL DEFAULT 0,
    accuracy        REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS attempts (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id     INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    session_id     INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
    activity_code  TEXT NOT NULL,
    step_index     INTEGER NOT NULL,
    expected       TEXT NOT NULL,
    detected       TEXT,
    confidence     REAL NOT NULL DEFAULT 0,
    correct        INTEGER NOT NULL DEFAULT 0,
    reaction_ms    INTEGER NOT NULL DEFAULT 0,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    at             REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_attempts_profile ON attempts(profile_id, at);
CREATE INDEX IF NOT EXISTS idx_attempts_expected ON attempts(profile_id, expected);

CREATE TABLE IF NOT EXISTS activity_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id      INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    session_id      INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
    activity_code   TEXT NOT NULL,
    accuracy        REAL NOT NULL,
    rhythm          REAL NOT NULL DEFAULT 0,
    gesture_quality REAL NOT NULL DEFAULT 0,
    stars           INTEGER NOT NULL DEFAULT 0,
    score           INTEGER NOT NULL DEFAULT 0,
    max_combo       INTEGER NOT NULL DEFAULT 0,
    duration_s      REAL NOT NULL DEFAULT 0,
    steps_total     INTEGER NOT NULL DEFAULT 0,
    steps_correct   INTEGER NOT NULL DEFAULT 0,
    at              REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_results_profile ON activity_results(profile_id, at);

CREATE TABLE IF NOT EXISTS rewards (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    kind       TEXT NOT NULL,
    code       TEXT NOT NULL,
    label      TEXT NOT NULL,
    icon       TEXT NOT NULL DEFAULT '⭐',
    at         REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS achievements (
    code        TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    description TEXT NOT NULL,
    icon        TEXT NOT NULL DEFAULT '🏆'
);

CREATE TABLE IF NOT EXISTS profile_achievements (
    profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    code       TEXT NOT NULL REFERENCES achievements(code) ON DELETE CASCADE,
    at         REAL NOT NULL,
    PRIMARY KEY (profile_id, code)
);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


class Database:
    """Conexión SQLite con un bloqueo por hilo.

    SQLite en modo WAL admite lecturas concurrentes; las escrituras se
    serializan con un mutex porque el hilo de la cámara puede registrar
    intentos mientras la interfaz consulta el progreso.
    """

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else db_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    # ---------------------------------------------------------------- básicos
    def execute(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        with self._lock:
            cur = self._conn.execute(sql, tuple(params))
            self._conn.commit()
            return cur

    def executemany(self, sql: str, seq: Iterable[Iterable[Any]]) -> None:
        with self._lock:
            self._conn.executemany(sql, [tuple(s) for s in seq])
            self._conn.commit()

    def query(self, sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, tuple(params)).fetchall()

    def one(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Row | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def scalar(self, sql: str, params: Iterable[Any] = (), default: Any = None) -> Any:
        row = self.one(sql, params)
        return row[0] if row is not None else default

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    # ---------------------------------------------------------------- meta
    def get_meta(self, key: str, default: str | None = None) -> str | None:
        row = self.one("SELECT value FROM meta WHERE key = ?", (key,))
        return row["value"] if row else default

    def set_meta(self, key: str, value: str) -> None:
        self.execute(
            "INSERT INTO meta(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


_db: Database | None = None


def get_db() -> Database:
    global _db
    if _db is None:
        _db = Database()
    return _db


def set_db(db: Database | None) -> None:
    global _db
    _db = db
