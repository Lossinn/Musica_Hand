"""`cumple` = la regla está IMPUESTA por la base de datos (True) o no (False).
Pruebas de integridad sobre el esquema REAL de HandSingKids7 (clase Database).

Comprueba, con evidencia ejecutable, qué reglas de calidad están realmente
impuestas por el código y cuáles no. Resultado: auditoria_calidad.json
"""
import json
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT))
from handsingkids.data.database import Database  # noqa: E402

res = []


def caso(id_, regla, esperado, fn):
    try:
        obs = fn()
        ok = obs[0]
        detalle = obs[1]
    except sqlite3.IntegrityError as e:
        ok, detalle = (esperado == "rechaza"), f"IntegrityError: {e}"
    except Exception as e:  # noqa: BLE001
        ok, detalle = False, f"{type(e).__name__}: {e}"
    res.append(dict(id=id_, regla=regla, esperado=esperado, cumple=bool(ok), detalle=str(detalle)[:140]))


with tempfile.TemporaryDirectory() as tmp:
    db = Database(Path(tmp) / "auditoria.sqlite3")
    now = time.time()
    db.execute("INSERT INTO profiles(name, age, avatar, created_at, last_seen_at) VALUES('Prueba', 7, 'iguana', ?, ?)", (now, now))
    pid = db.scalar("SELECT id FROM profiles")
    db.execute("INSERT INTO skills(code, name, level, difficulty) VALUES('nota_DO3', 'Do', 1, 0.1)")

    caso("Q1", "Modo de registro WAL", "wal",
         lambda: ((m := db.scalar("PRAGMA journal_mode")) == "wal", f"journal_mode = {m}"))
    caso("Q2", "Llaves foráneas activas (intento con perfil inexistente)", "rechaza",
         lambda: (db.execute("INSERT INTO attempts(profile_id, activity_code, step_index, expected, at) VALUES(999,'a',0,'DO3',?)", (now,)) and False, "aceptó"))
    caso("Q3", "NOT NULL en profiles.name", "rechaza",
         lambda: (db.execute("INSERT INTO profiles(name, age, avatar, created_at, last_seen_at) VALUES(NULL, 7, 'x', ?, ?)", (now, now)) and False, "aceptó"))
    caso("Q4", "Rango de edad 3-12 en la base (age = 99)", "rechaza",
         lambda: (db.execute("INSERT INTO profiles(name, age, avatar, created_at, last_seen_at) VALUES('Fuera', 99, 'x', ?, ?)", (now, now)).rowcount != 1,
                  "la base acepta age = 99 (no hay CHECK)"))
    caso("Q5", "Rango de attempts.confidence en [0,1] (valor 5.0) y correct en {0,1} (valor 7)", "rechaza",
         lambda: (db.execute("INSERT INTO attempts(profile_id, activity_code, step_index, expected, confidence, correct, at) VALUES(?,?,0,'DO3',5.0,7,?)", (pid, 'a', now)).rowcount != 1,
                  "la base acepta confidence = 5.0 y correct = 7 (no hay CHECK)"))
    caso("Q6", "skill_state.mastery en [0,1] (valor -3)", "rechaza",
         lambda: (db.execute("INSERT INTO skill_state(profile_id, skill_code, mastery) VALUES(?, 'nota_DO3', -3)", (pid,)).rowcount != 1,
                  "la base acepta mastery = -3 (no hay CHECK)"))
    # cascada
    db.execute("INSERT INTO sessions(profile_id, started_at) VALUES(?, ?)", (pid, now))
    db.execute("INSERT INTO activity_results(profile_id, activity_code, accuracy, at) VALUES(?, 'a', 80, ?)", (pid, now))
    antes = {t: db.scalar(f"SELECT COUNT(*) FROM {t} WHERE profile_id = ?", (pid,))
             for t in ("skill_state", "attempts", "activity_results", "sessions")}
    db.execute("DELETE FROM profiles WHERE id = ?", (pid,))
    desp = {t: db.scalar(f"SELECT COUNT(*) FROM {t} WHERE profile_id = ?", (pid,))
            for t in antes}
    caso("Q7", "Borrado en cascada de los datos del perfil en la base", "cumple",
         lambda: (all(v == 0 for v in desp.values()) and all(v > 0 for v in antes.values()),
                  f"antes {antes} → después {desp}"))
    db.close()

# Plantillas (archivos) tras borrar el perfil: el código no las elimina
src = (ROOT / "handsingkids" / "data" / "repositories.py").read_text(encoding="utf-8")
borra_archivos = "unlink" in src.split("def delete")[1].split("def ")[0]
res.append(dict(id="Q8", regla="El borrado de un perfil elimina también gestos/perfil_<id>.json y melodias/*.json",
                esperado="cumple", cumple=borra_archivos,
                detalle="ProfileRepository.delete solo ejecuta DELETE FROM profiles; no elimina archivos"))
out = dict(resultados=res, cumplen=sum(r["cumple"] for r in res), total=len(res))
Path(__file__).with_name("auditoria_calidad.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for r in res:
    print(("OK   " if r["cumple"] else "FALLA"), r["id"], r["regla"], "→", r["detalle"])
