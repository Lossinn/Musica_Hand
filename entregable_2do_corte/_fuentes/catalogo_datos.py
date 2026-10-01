"""Extrae el catálogo de datos REAL desde el esquema de HandSingKids7 (PRAGMA de SQLite).
Así el diccionario del documento no puede diferir del código."""
import json, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT))
from handsingkids.data.database import SCHEMA

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
out = {}
for (t,) in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by rowid"):
    cols = [dict(cid=r[0], nombre=r[1], tipo=r[2], not_null=bool(r[3]), defecto=r[4], pk=bool(r[5]))
            for r in con.execute(f"pragma table_info({t})")]
    fks = [dict(col=r[3], ref_tabla=r[2], ref_col=r[4], on_delete=r[6]) for r in con.execute(f"pragma foreign_key_list({t})")]
    idx = [r[1] for r in con.execute(f"pragma index_list({t})") if not r[1].startswith("sqlite_autoindex")]
    out[t] = dict(columnas=cols, fks=fks, indices=idx)
ddl = SCHEMA.upper()
out["_resumen"] = dict(tablas=len([k for k in out if not k.startswith("_")]),
                       columnas=sum(len(v["columnas"]) for k, v in out.items() if not k.startswith("_")),
                       check_constraints=ddl.count("CHECK"), wal="JOURNAL_MODE = WAL" in ddl, foreign_keys="FOREIGN_KEYS = ON" in ddl)
json.dump(out, open("catalogo_datos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out["_resumen"])
for t, v in out.items():
    if t.startswith("_"): continue
    print(f"{t}: " + ", ".join(f"{c['nombre']}:{c['tipo']}{'*' if c['pk'] else ''}{'!' if c['not_null'] else ''}" for c in v["columnas"]))
    if v["fks"]: print("   FK:", [(f['col'], f['ref_tabla'], f['on_delete']) for f in v["fks"]])
