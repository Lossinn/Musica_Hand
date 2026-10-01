"""Repositorios: traducen entre filas de SQLite y entidades del dominio."""

from __future__ import annotations

import json
import sqlite3
import time
from datetime import date, timedelta

from ..domain.entities import (Achievement, Activity, ActivityKind, ActivityResult,
                               Attempt, LearningSession, PlayMode, Profile, Reward,
                               Skill, SkillState, SkillStatus)
from .database import Database, get_db


def _loads(value: str | None, default):
    if not value:
        return default
    try:
        return json.loads(value)
    except Exception:
        return default


# ---------------------------------------------------------------- perfiles

class ProfileRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    @staticmethod
    def _to_entity(r: sqlite3.Row) -> Profile:
        return Profile(
            id=r["id"], name=r["name"], age=r["age"], avatar=r["avatar"],
            created_at=r["created_at"], last_seen_at=r["last_seen_at"],
            stars=r["stars"], coins=r["coins"], streak_days=r["streak_days"],
            last_play_date=r["last_play_date"], calibrated=bool(r["calibrated"]),
        )

    def all(self) -> list[Profile]:
        rows = self.db.query("SELECT * FROM profiles ORDER BY last_seen_at DESC")
        return [self._to_entity(r) for r in rows]

    def get(self, profile_id: int) -> Profile | None:
        r = self.db.one("SELECT * FROM profiles WHERE id = ?", (profile_id,))
        return self._to_entity(r) if r else None

    def create(self, name: str, age: int, avatar: str = "iguana") -> Profile:
        now = time.time()
        cur = self.db.execute(
            "INSERT INTO profiles(name, age, avatar, created_at, last_seen_at) "
            "VALUES(?,?,?,?,?)", (name.strip(), int(age), avatar, now, now))
        return self.get(int(cur.lastrowid))  # type: ignore[arg-type]

    def save(self, p: Profile) -> None:
        self.db.execute(
            "UPDATE profiles SET name=?, age=?, avatar=?, last_seen_at=?, stars=?, "
            "coins=?, streak_days=?, last_play_date=?, calibrated=? WHERE id=?",
            (p.name, p.age, p.avatar, p.last_seen_at, p.stars, p.coins,
             p.streak_days, p.last_play_date, int(p.calibrated), p.id))

    def delete(self, profile_id: int) -> None:
        self.db.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))

    def touch(self, p: Profile) -> Profile:
        """Actualiza la última visita y la racha de días consecutivos."""
        today = date.today()
        today_s = today.isoformat()
        if p.last_play_date != today_s:
            yesterday = (today - timedelta(days=1)).isoformat()
            p.streak_days = p.streak_days + 1 if p.last_play_date == yesterday else 1
            p.last_play_date = today_s
        p.last_seen_at = time.time()
        self.save(p)
        return p

    def add_stars(self, p: Profile, stars: int, coins: int = 0) -> None:
        p.stars += max(0, stars)
        p.coins += max(0, coins)
        self.save(p)


# ------------------------------------------------------------- habilidades

class SkillRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    @staticmethod
    def _to_entity(r: sqlite3.Row) -> Skill:
        return Skill(code=r["code"], name=r["name"], note_code=r["note_code"],
                     level=r["level"], difficulty=r["difficulty"],
                     prerequisites=_loads(r["prerequisites"], []),
                     order_index=r["order_index"], description=r["description"])

    def all(self) -> list[Skill]:
        rows = self.db.query("SELECT * FROM skills ORDER BY order_index, level")
        return [self._to_entity(r) for r in rows]

    def get(self, code: str) -> Skill | None:
        r = self.db.one("SELECT * FROM skills WHERE code = ?", (code,))
        return self._to_entity(r) if r else None

    def upsert_many(self, skills: list[Skill]) -> None:
        self.db.executemany(
            "INSERT INTO skills(code,name,note_code,level,difficulty,prerequisites,"
            "order_index,description) VALUES(?,?,?,?,?,?,?,?) "
            "ON CONFLICT(code) DO UPDATE SET name=excluded.name, "
            "note_code=excluded.note_code, level=excluded.level, "
            "difficulty=excluded.difficulty, prerequisites=excluded.prerequisites, "
            "order_index=excluded.order_index, description=excluded.description",
            [(s.code, s.name, s.note_code, s.level, s.difficulty,
              json.dumps(s.prerequisites), s.order_index, s.description)
             for s in skills])


class SkillStateRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    @staticmethod
    def _to_entity(r: sqlite3.Row) -> SkillState:
        return SkillState(
            profile_id=r["profile_id"], skill_code=r["skill_code"],
            status=SkillStatus(r["status"]), mastery=r["mastery"],
            precision=r["precision_v"], consistency=r["consistency"],
            speed=r["speed"], retention=r["retention"], attempts=r["attempts"],
            hits=r["hits"], mean_reaction_ms=r["mean_reaction_ms"],
            last_practice_at=r["last_practice_at"], due_at=r["due_at"],
            ease=r["ease"], interval_days=r["interval_days"])

    def for_profile(self, profile_id: int) -> dict[str, SkillState]:
        rows = self.db.query("SELECT * FROM skill_state WHERE profile_id = ?",
                             (profile_id,))
        return {r["skill_code"]: self._to_entity(r) for r in rows}

    def get(self, profile_id: int, skill_code: str) -> SkillState:
        r = self.db.one(
            "SELECT * FROM skill_state WHERE profile_id=? AND skill_code=?",
            (profile_id, skill_code))
        if r:
            return self._to_entity(r)
        state = SkillState(profile_id=profile_id, skill_code=skill_code)
        self.save(state)
        return state

    def save(self, s: SkillState) -> None:
        self.db.execute(
            "INSERT INTO skill_state(profile_id,skill_code,status,mastery,precision_v,"
            "consistency,speed,retention,attempts,hits,mean_reaction_ms,"
            "last_practice_at,due_at,ease,interval_days) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(profile_id,skill_code) DO UPDATE SET "
            "status=excluded.status, mastery=excluded.mastery, "
            "precision_v=excluded.precision_v, consistency=excluded.consistency, "
            "speed=excluded.speed, retention=excluded.retention, "
            "attempts=excluded.attempts, hits=excluded.hits, "
            "mean_reaction_ms=excluded.mean_reaction_ms, "
            "last_practice_at=excluded.last_practice_at, due_at=excluded.due_at, "
            "ease=excluded.ease, interval_days=excluded.interval_days",
            (s.profile_id, s.skill_code, s.status.value, s.mastery, s.precision,
             s.consistency, s.speed, s.retention, s.attempts, s.hits,
             s.mean_reaction_ms, s.last_practice_at, s.due_at, s.ease,
             s.interval_days))

    def initialize(self, profile_id: int, skills: list[Skill]) -> None:
        """Crea el estado inicial: las habilidades sin prerrequisitos quedan
        introducidas y el resto bloqueadas."""
        for sk in skills:
            st = SkillState(profile_id=profile_id, skill_code=sk.code)
            st.status = (SkillStatus.INTRODUCED if not sk.prerequisites
                         else SkillStatus.LOCKED)
            self.save(st)


# ------------------------------------------------------------- actividades

class ActivityRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    @staticmethod
    def _to_entity(r: sqlite3.Row) -> Activity:
        return Activity(
            code=r["code"], kind=ActivityKind(r["kind"]), title=r["title"],
            level=r["level"], difficulty=r["difficulty"],
            skill_codes=_loads(r["skill_codes"], []),
            sequence=_loads(r["sequence"], []), mode=PlayMode(r["mode"]),
            tempo_bpm=r["tempo_bpm"], duration_s=r["duration_s"],
            hints=bool(r["hints"]), repetitions=r["repetitions"],
            description=r["description"], icon=r["icon"],
            tolerance_ms=r["tolerance_ms"])

    def all(self) -> list[Activity]:
        rows = self.db.query("SELECT * FROM activities ORDER BY level, difficulty")
        return [self._to_entity(r) for r in rows]

    def get(self, code: str) -> Activity | None:
        r = self.db.one("SELECT * FROM activities WHERE code = ?", (code,))
        return self._to_entity(r) if r else None

    def by_level(self, level: int) -> list[Activity]:
        rows = self.db.query(
            "SELECT * FROM activities WHERE level = ? ORDER BY difficulty", (level,))
        return [self._to_entity(r) for r in rows]

    def by_kind(self, kind: ActivityKind) -> list[Activity]:
        rows = self.db.query(
            "SELECT * FROM activities WHERE kind = ? ORDER BY level, difficulty",
            (kind.value,))
        return [self._to_entity(r) for r in rows]

    def upsert_many(self, activities: list[Activity]) -> None:
        self.db.executemany(
            "INSERT INTO activities(code,kind,title,level,difficulty,skill_codes,"
            "sequence,mode,tempo_bpm,duration_s,hints,repetitions,description,icon,"
            "tolerance_ms) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(code) DO UPDATE SET kind=excluded.kind, title=excluded.title,"
            " level=excluded.level, difficulty=excluded.difficulty, "
            "skill_codes=excluded.skill_codes, sequence=excluded.sequence, "
            "mode=excluded.mode, tempo_bpm=excluded.tempo_bpm, "
            "duration_s=excluded.duration_s, hints=excluded.hints, "
            "repetitions=excluded.repetitions, description=excluded.description, "
            "icon=excluded.icon, tolerance_ms=excluded.tolerance_ms",
            [(a.code, a.kind.value, a.title, a.level, a.difficulty,
              json.dumps(a.skill_codes), json.dumps(a.sequence), a.mode.value,
              a.tempo_bpm, a.duration_s, int(a.hints), a.repetitions,
              a.description, a.icon, a.tolerance_ms) for a in activities])


# ------------------------------------------------ intentos, sesiones, logros

class AttemptRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    def add(self, a: Attempt) -> Attempt:
        cur = self.db.execute(
            "INSERT INTO attempts(profile_id,session_id,activity_code,step_index,"
            "expected,detected,confidence,correct,reaction_ms,attempt_number,at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (a.profile_id, a.session_id, a.activity_code, a.step_index, a.expected,
             a.detected, a.confidence, int(a.correct), a.reaction_ms,
             a.attempt_number, a.at))
        a.id = int(cur.lastrowid)  # type: ignore[arg-type]
        return a

    def recent_for_note(self, profile_id: int, note_code: str,
                        limit: int = 20) -> list[sqlite3.Row]:
        return self.db.query(
            "SELECT * FROM attempts WHERE profile_id=? AND expected=? "
            "ORDER BY at DESC LIMIT ?", (profile_id, note_code, limit))

    def accuracy_by_note(self, profile_id: int) -> dict[str, tuple[int, int]]:
        rows = self.db.query(
            "SELECT expected, COUNT(*) n, SUM(correct) h FROM attempts "
            "WHERE profile_id=? GROUP BY expected", (profile_id,))
        return {r["expected"]: (int(r["h"] or 0), int(r["n"])) for r in rows}

    def confusion_pairs(self, profile_id: int, limit: int = 8) -> list[tuple[str, str, int]]:
        rows = self.db.query(
            "SELECT expected, detected, COUNT(*) n FROM attempts "
            "WHERE profile_id=? AND correct=0 AND detected IS NOT NULL "
            "GROUP BY expected, detected ORDER BY n DESC LIMIT ?",
            (profile_id, limit))
        return [(r["expected"], r["detected"], int(r["n"])) for r in rows]

    def total(self, profile_id: int) -> int:
        return int(self.db.scalar(
            "SELECT COUNT(*) FROM attempts WHERE profile_id=?", (profile_id,), 0))

    def training_rows(self, profile_id: int) -> list[dict]:
        """Intentos reales de este niño, listos para entrenar el predictor.

        Cada fila lleva la precisión y los días desde la última práctica de
        esa nota **calculados solo con lo que ya había pasado antes de ese
        intento** (nunca con el resultado del propio intento ni con los
        siguientes): son exactamente las mismas cantidades que
        `learning.mastery` guarda en `SkillState`, así que un modelo
        entrenado con esto predice sobre las mismas variables que ve en
        producción. No hay ningún dato inventado: todo sale de la tabla
        `attempts` tal como quedó registrada mientras el niño jugaba.
        """
        from ..learning.mastery import precision as _precision

        filas = self.db.query(
            "SELECT a.expected, a.correct, a.at, "
            "COALESCE(act.difficulty, 0.3) AS act_difficulty "
            "FROM attempts a LEFT JOIN activities act "
            "ON act.code = a.activity_code "
            "WHERE a.profile_id = ? ORDER BY a.at ASC", (profile_id,))

        hits: dict[str, int] = {}
        intentos: dict[str, int] = {}
        ultimo_at: dict[str, float] = {}
        out: list[dict] = []
        for r in filas:
            nota = r["expected"]
            h, n = hits.get(nota, 0), intentos.get(nota, 0)
            dias = ((r["at"] - ultimo_at[nota]) / 86400.0
                    if nota in ultimo_at else 0.0)
            out.append({
                "correct": bool(r["correct"]),
                "precision_nota": _precision(h, n),
                "dificultad": float(r["act_difficulty"]),
                "dias_desde_ultima": max(0.0, min(14.0, dias)),
            })
            hits[nota] = h + int(r["correct"])
            intentos[nota] = n + 1
            ultimo_at[nota] = r["at"]
        return out


class ResultRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    def add(self, r: ActivityResult) -> ActivityResult:
        cur = self.db.execute(
            "INSERT INTO activity_results(profile_id,session_id,activity_code,accuracy,"
            "rhythm,gesture_quality,stars,score,max_combo,duration_s,steps_total,"
            "steps_correct,at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (r.profile_id, r.session_id, r.activity_code, r.accuracy, r.rhythm,
             r.gesture_quality, r.stars, r.score, r.max_combo, r.duration_s,
             r.steps_total, r.steps_correct, r.at))
        r.id = int(cur.lastrowid)  # type: ignore[arg-type]
        return r

    def best_stars(self, profile_id: int, activity_code: str) -> int:
        return int(self.db.scalar(
            "SELECT MAX(stars) FROM activity_results WHERE profile_id=? AND "
            "activity_code=?", (profile_id, activity_code), 0) or 0)

    def stars_by_activity(self, profile_id: int) -> dict[str, int]:
        rows = self.db.query(
            "SELECT activity_code, MAX(stars) s FROM activity_results "
            "WHERE profile_id=? GROUP BY activity_code", (profile_id,))
        return {r["activity_code"]: int(r["s"] or 0) for r in rows}

    def history(self, profile_id: int, limit: int = 60) -> list[sqlite3.Row]:
        return self.db.query(
            "SELECT * FROM activity_results WHERE profile_id=? ORDER BY at DESC "
            "LIMIT ?", (profile_id, limit))

    def weekly_minutes(self, profile_id: int) -> float:
        since = time.time() - 7 * 86400
        secs = self.db.scalar(
            "SELECT SUM(duration_s) FROM activity_results WHERE profile_id=? AND at>=?",
            (profile_id, since), 0) or 0
        return round(float(secs) / 60.0, 1)

    def count_since(self, profile_id: int, since: float) -> int:
        return int(self.db.scalar(
            "SELECT COUNT(*) FROM activity_results WHERE profile_id=? AND at>=?",
            (profile_id, since), 0))


class SessionRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    def start(self, profile_id: int) -> LearningSession:
        s = LearningSession(profile_id=profile_id)
        cur = self.db.execute(
            "INSERT INTO sessions(profile_id, started_at) VALUES(?,?)",
            (profile_id, s.started_at))
        s.id = int(cur.lastrowid)  # type: ignore[arg-type]
        return s

    def end(self, s: LearningSession) -> None:
        s.ended_at = time.time()
        self.db.execute(
            "UPDATE sessions SET ended_at=?, activities_done=?, accuracy=? WHERE id=?",
            (s.ended_at, s.activities_done, s.accuracy, s.id))


class RewardRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    def add(self, r: Reward) -> Reward:
        cur = self.db.execute(
            "INSERT INTO rewards(profile_id,kind,code,label,icon,at) VALUES(?,?,?,?,?,?)",
            (r.profile_id, r.kind, r.code, r.label, r.icon, r.at))
        r.id = int(cur.lastrowid)  # type: ignore[arg-type]
        return r

    def recent(self, profile_id: int, limit: int = 12) -> list[sqlite3.Row]:
        return self.db.query(
            "SELECT * FROM rewards WHERE profile_id=? ORDER BY at DESC LIMIT ?",
            (profile_id, limit))


class AchievementRepository:
    def __init__(self, db: Database | None = None) -> None:
        self.db = db or get_db()

    def upsert_many(self, items: list[Achievement]) -> None:
        self.db.executemany(
            "INSERT INTO achievements(code,title,description,icon) VALUES(?,?,?,?) "
            "ON CONFLICT(code) DO UPDATE SET title=excluded.title, "
            "description=excluded.description, icon=excluded.icon",
            [(a.code, a.title, a.description, a.icon) for a in items])

    def all(self) -> list[Achievement]:
        return [Achievement(code=r["code"], title=r["title"],
                            description=r["description"], icon=r["icon"])
                for r in self.db.query("SELECT * FROM achievements ORDER BY code")]

    def unlocked(self, profile_id: int) -> set[str]:
        return {r["code"] for r in self.db.query(
            "SELECT code FROM profile_achievements WHERE profile_id=?", (profile_id,))}

    def unlock(self, profile_id: int, code: str) -> bool:
        """Devuelve True si es la primera vez que se desbloquea."""
        if code in self.unlocked(profile_id):
            return False
        self.db.execute(
            "INSERT OR IGNORE INTO profile_achievements(profile_id,code,at) "
            "VALUES(?,?,?)", (profile_id, code, time.time()))
        return True
