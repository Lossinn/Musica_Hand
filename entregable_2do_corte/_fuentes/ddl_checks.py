"""Construye y prueba la migración propuesta de restricciones CHECK sobre el esquema real."""
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT))
from handsingkids.data.database import SCHEMA  # noqa: E402

REGLAS = [  # (columna, tabla, expresión CHECK)
    ("age", "profiles", "CHECK (age BETWEEN 3 AND 12)"),
    ("stars", "profiles", "CHECK (stars >= 0)"),
    ("coins", "profiles", "CHECK (coins >= 0)"),
    ("streak_days", "profiles", "CHECK (streak_days >= 0)"),
    ("calibrated", "profiles", "CHECK (calibrated IN (0, 1))"),
    ("status", "skill_state", "CHECK (status IN ('bloqueada','introducida','en_practica','dominada','consolidada'))"),
    ("mastery", "skill_state", "CHECK (mastery BETWEEN 0 AND 1)"),
    ("precision_v", "skill_state", "CHECK (precision_v BETWEEN 0 AND 1)"),
    ("consistency", "skill_state", "CHECK (consistency BETWEEN 0 AND 1)"),
    ("speed", "skill_state", "CHECK (speed BETWEEN 0 AND 1)"),
    ("retention", "skill_state", "CHECK (retention BETWEEN 0 AND 1)"),
    ("confidence", "attempts", "CHECK (confidence BETWEEN 0 AND 1)"),
    ("correct", "attempts", "CHECK (correct IN (0, 1))"),
    ("reaction_ms", "attempts", "CHECK (reaction_ms >= 0)"),
    ("accuracy", "activity_results", "CHECK (accuracy BETWEEN 0 AND 100)"),
    ("stars", "activity_results", "CHECK (stars BETWEEN 0 AND 3)"),
]
nuevo = SCHEMA
for col, tabla, chk in REGLAS:
    # localizar el bloque de la tabla y la línea de la columna dentro de él
    m = re.search(rf"CREATE TABLE IF NOT EXISTS {tabla} \((.*?)\n\);", nuevo, re.S)
    bloque = m.group(0)
    linea = re.search(rf"^(\s+{col}\s+\S+[^\n,]*?)(,?)$", bloque, re.M)
    assert linea, (tabla, col)
    nuevo_bloque = bloque.replace(linea.group(0), f"{linea.group(1)} {chk}{linea.group(2)}", 1)
    nuevo = nuevo.replace(bloque, nuevo_bloque, 1)
Path(__file__).with_name("propuesta_check.sql").write_text(nuevo, encoding="utf-8")

con = sqlite3.connect(":memory:")
con.executescript(nuevo)
ahora = time.time()
casos = [
    ("perfil válido (edad 7)", "INSERT INTO profiles(name,age,avatar,created_at,last_seen_at) VALUES('A',7,'x',?,?)", (ahora, ahora), True),
    ("edad 99", "INSERT INTO profiles(name,age,avatar,created_at,last_seen_at) VALUES('B',99,'x',?,?)", (ahora, ahora), False),
    ("edad 2", "INSERT INTO profiles(name,age,avatar,created_at,last_seen_at) VALUES('C',2,'x',?,?)", (ahora, ahora), False),
    ("confianza 5,0", "INSERT INTO attempts(profile_id,activity_code,step_index,expected,confidence,correct,at) VALUES(1,'a',0,'DO3',5.0,1,?)", (ahora,), False),
    ("correct = 7", "INSERT INTO attempts(profile_id,activity_code,step_index,expected,confidence,correct,at) VALUES(1,'a',0,'DO3',0.8,7,?)", (ahora,), False),
    ("intento válido", "INSERT INTO attempts(profile_id,activity_code,step_index,expected,confidence,correct,at) VALUES(1,'a',0,'DO3',0.8,1,?)", (ahora,), True),
    ("estado inválido", "INSERT INTO skills(code,name,level,difficulty) VALUES('s','s',1,0.1)", (), True),
    ("mastery -3", "INSERT INTO skill_state(profile_id,skill_code,mastery) VALUES(1,'s',-3)", (), False),
    ("estado 'practicando' (valor que usaba el documento previo)", "INSERT INTO skill_state(profile_id,skill_code,status) VALUES(1,'s','practicando')", (), False),
    ("estado 'en_practica' (valor real)", "INSERT INTO skill_state(profile_id,skill_code,status,mastery) VALUES(1,'s','en_practica',0.5)", (), True),
]
res = []
for nombre, sql, par, debe_aceptar in casos:
    if nombre == "estado inválido":      # fila auxiliar para la FK, no es un caso de prueba
        con.execute(sql, par); continue
    try:
        con.execute(sql, par); aceptó = True
    except sqlite3.IntegrityError:
        aceptó = False
    res.append(dict(caso=nombre, esperado="acepta" if debe_aceptar else "rechaza", obtenido="acepta" if aceptó else "rechaza",
                    correcto=aceptó == debe_aceptar))
# datos reales de la aplicación (semilla + intentos de demostración) deben seguir siendo válidos con las restricciones
from handsingkids.data.database import Database  # noqa: E402
import tempfile
from handsingkids.data import seed
db = Database(Path(tempfile.mkdtemp()) / "s.sqlite3")
seed.seed(db)
ok_semilla = db.scalar("SELECT COUNT(*) FROM skills") > 0
out = dict(reglas=len(REGLAS), resultados=res, todos_correctos=all(r["correcto"] for r in res), semilla_ok=ok_semilla)
Path(__file__).with_name("ddl_checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for r in res:
    print("OK   " if r["correcto"] else "FALLA", r["caso"], "->", r["obtenido"])
print("reglas:", len(REGLAS), "| todos correctos:", out["todos_correctos"])
