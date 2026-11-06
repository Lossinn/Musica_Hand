"""Sensibilidad de la decisión de aceptación (umbral de distancia, confianza y margen) sobre el protocolo de evidencia_vision.py.
Se varía un umbral por vez; el resto queda en su valor por defecto. Mismas semillas y construcción que benchmark_aciertos / falsos_positivos.
Salida: sensibilidad_umbrales.json. Uso: python -X utf8 sensibilidad_umbrales.py"""
import json, sys
from pathlib import Path
import numpy as np
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(RAIZ)); sys.path.insert(0, str(RAIZ / "tests"))
import test_vision as tv
from handsingkids.vision.classifier import GestureClassifier
from handsingkids.vision.features import pose_features
from handsingkids.vision.templates import TemplateStore

def wilson(k, n, z=1.959964):
    import math
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - m), 100 * (c + m)

def medir(**kw):
    raw = tv.load_fixture(); store = TemplateStore(0)
    for code, e in raw.items(): store.add_sample(code, e["hands"])
    clf = GestureClassifier(store, **kw); clf.calibrate_temperature()
    out = {}
    for noise in (0.06, 0.09):
        rng = np.random.default_rng(11); ok = tot = 0
        # replica el orden de sorteo de benchmark_aciertos: recorre los niveles en orden; para alinear semillas se recorren todos
        out[noise] = None
    rng = np.random.default_rng(11); res = {}
    for noise in (0.0, 0.03, 0.06, 0.09):
        ok = tot = 0
        for code, e in raw.items():
            for _ in range(60):
                h = tv.perturb(e["hands"], rng, noise=noise, scale=float(rng.uniform(0.8, 1.25)))
                tot += 1; ok += clf.classify(pose_features(h)).note == code
        res[noise] = (ok, tot)
    rng = np.random.default_rng(23); codes = list(raw); fp = n = 0
    for _ in range(40):
        for i, a in enumerate(codes):
            b = codes[(i + 3) % len(codes)]
            for pose in (tv.transition(raw[a]["hands"], raw[b]["hands"], 0.5), tv.chimera(raw[a]["hands"], raw[b]["hands"])):
                pose = tv.perturb(pose, rng, noise=0.02, scale=float(rng.uniform(0.9, 1.15)))
                n += 1; fp += clf.classify(pose_features(pose)).note is not None
    return {"ac_0": 100 * res[0.0][0] / res[0.0][1], "ac_006": 100 * res[0.06][0] / res[0.06][1], "ac_009": 100 * res[0.09][0] / res[0.09][1],
            "fp": 100 * fp / n, "fp_k": fp, "fp_n": n, "fp_ic": wilson(fp, n)}

malla = {"max_distance": [0.65, 0.80, 0.95, 1.10, 1.25], "confidence_threshold": [0.35, 0.45, 0.55, 0.65, 0.75], "margin_threshold": [0.00, 0.04, 0.08, 0.12, 0.16]}
sal = {"base": medir()}
for par, vals in malla.items():
    sal[par] = [dict(valor=v, **medir(**{par: v})) for v in vals]
(AQUI / "sensibilidad_umbrales.json").write_text(json.dumps(sal, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(sal["base"]))
for par in malla:
    print(par)
    for r in sal[par]: print("  ", r["valor"], round(r["ac_009"], 1), round(r["ac_006"], 1), round(r["fp"], 1))
