"""Contrasta con el código real las afirmaciones técnicas del estudio PINT2 (Equipo 13)."""
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
out = {}

# 1) dependencias y menciones en el código
fuentes = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in (ROOT / "handsingkids").rglob("*.py"))
req = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
for nombre in ("gemini", "simpy", "scipy", "streamlit", "gradio", "google.generativeai", "pyside6", "mediapipe", "pulp"):
    out[f"codigo_menciona_{nombre}"] = bool(re.search(nombre, fuentes, re.I))
    out[f"requirements_{nombre}"] = nombre in req

# 2) tiempo de resolución del planificador
import test_optimizer as T  # noqa: E402
from handsingkids.intelligence.optimizer import SessionOptimizer  # noqa: E402

cand = T._candidatas()
est = T._estados(ajustes={"nota_MI3": 0.3, "nota_FA3": 0.45})
for etiqueta, milp in (("milp_cbc", True), ("enumeracion_exacta", False)):
    ts = []
    for _ in range(15):
        t0 = time.perf_counter()
        r = SessionOptimizer(budget_minutes=8, session_size=4, prefer_milp=milp).solve(cand, est)
        ts.append((time.perf_counter() - t0) * 1e3)
    out[f"solver_{etiqueta}_ms"] = dict(metodo=r.method, media=round(statistics.mean(ts), 1), min=round(min(ts), 1), max=round(max(ts), 1),
                                         candidatas=len(cand))

# 3) fps y estados de habilidad
from handsingkids.core.config import VisionSettings  # noqa: E402
out["target_fps_defecto"] = VisionSettings().target_fps
from handsingkids.domain.entities import SkillStatus  # noqa: E402
out["estados_habilidad"] = [s.value for s in SkillStatus]

Path(__file__).with_name("contraste_pint2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
