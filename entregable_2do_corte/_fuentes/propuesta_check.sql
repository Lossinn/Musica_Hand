
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS profiles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    age             INTEGER NOT NULL CHECK (age BETWEEN 3 AND 12),
    avatar          TEXT NOT NULL DEFAULT 'iguana',
    created_at      REAL NOT NULL,
    last_seen_at    REAL NOT NULL,
    stars           INTEGER NOT NULL DEFAULT 0 CHECK (stars >= 0),
    coins           INTEGER NOT NULL DEFAULT 0 CHECK (coins >= 0),
    streak_days     INTEGER NOT NULL DEFAULT 0 CHECK (streak_days >= 0),
    last_play_date  TEXT NOT NULL DEFAULT '',
    calibrated      INTEGER NOT NULL DEFAULT 0 CHECK (calibrated IN (0, 1))
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
    status           TEXT NOT NULL DEFAULT 'bloqueada' CHECK (status IN ('bloqueada','introducida','en_practica','dominada','consolidada')),
    mastery          REAL NOT NULL DEFAULT 0 CHECK (mastery BETWEEN 0 AND 1),
    precision_v      REAL NOT NULL DEFAULT 0 CHECK (precision_v BETWEEN 0 AND 1),
    consistency      REAL NOT NULL DEFAULT 0 CHECK (consistency BETWEEN 0 AND 1),
    speed            REAL NOT NULL DEFAULT 0 CHECK (speed BETWEEN 0 AND 1),
    retention        REAL NOT NULL DEFAULT 1 CHECK (retention BETWEEN 0 AND 1),
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
    confidence     REAL NOT NULL DEFAULT 0 CHECK (confidence BETWEEN 0 AND 1),
    correct        INTEGER NOT NULL DEFAULT 0 CHECK (correct IN (0, 1)),
    reaction_ms    INTEGER NOT NULL DEFAULT 0 CHECK (reaction_ms >= 0),
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
    accuracy        REAL NOT NULL CHECK (accuracy BETWEEN 0 AND 100),
    rhythm          REAL NOT NULL DEFAULT 0,
    gesture_quality REAL NOT NULL DEFAULT 0,
    stars           INTEGER NOT NULL DEFAULT 0 CHECK (stars BETWEEN 0 AND 3),
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
