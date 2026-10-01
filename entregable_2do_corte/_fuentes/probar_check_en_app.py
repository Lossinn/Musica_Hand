"""Ejecuta las suites de integración y de capturas con el esquema CHECK propuesto."""
import json
import os
import runpy
import sys
from pathlib import Path

os.environ["QT_QPA_PLATFORM"] = "offscreen"
F = Path(__file__).parent
ROOT = F.parents[1] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
import handsingkids.data.database as D  # noqa: E402

D.SCHEMA = (F / "propuesta_check.sql").read_text(encoding="utf-8")
resultado = {}
for nombre in ("test_integracion.py", "test_mastery.py", "test_predictor.py"):
    try:
        runpy.run_path(str(ROOT / "tests" / nombre), run_name="__main__")
        resultado[nombre] = "terminó sin excepción"
    except SystemExit as e:
        resultado[nombre] = "pasó" if e.code in (0, None) else f"falló (código {e.code})"
    except Exception as e:  # noqa: BLE001
        resultado[nombre] = f"EXCEPCIÓN: {type(e).__name__}: {e}"
(F / "check_en_app.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
print("RESULTADO:", json.dumps(resultado, ensure_ascii=False))
os._exit(0)
