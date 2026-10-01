"""Mide la latencia del descriptor + clasificador (sin cámara ni interfaz) con la
calibración real del proyecto. Reproducible: python bench_latencia.py"""
import json, platform, statistics, sys, time
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from handsingkids.vision.classifier import GestureClassifier
from handsingkids.vision.features import pose_features
from handsingkids.vision.templates import TemplateStore
import test_vision as tv

raw = tv.load_fixture()
store = TemplateStore(0)
for code, entry in raw.items():
    store.add_sample(code, entry["hands"])
clf = GestureClassifier(store); clf.calibrate_temperature()
rng = np.random.default_rng(7)
frames = [tv.perturb(raw[c]["hands"], rng, noise=0.03, scale=float(rng.uniform(.8, 1.25)))
          for c in raw for _ in range(25)]
for f in frames[:20]:                       # calentamiento
    clf.classify(pose_features(f))
t_desc, t_clf, t_tot = [], [], []
for _ in range(5):
    for f in frames:
        a = time.perf_counter(); p = pose_features(f)
        b = time.perf_counter(); clf.classify(p); c = time.perf_counter()
        t_desc.append((b - a) * 1e3); t_clf.append((c - b) * 1e3); t_tot.append((c - a) * 1e3)
q = lambda x, p: float(np.percentile(x, p))
res = {"n_fotogramas": len(t_tot), "dim_descriptor": int(pose_features(frames[0]).vector.size),
       "descriptor_ms": {"media": statistics.mean(t_desc), "p95": q(t_desc, 95)},
       "clasificador_ms": {"media": statistics.mean(t_clf), "p95": q(t_clf, 95)},
       "total_ms": {"media": statistics.mean(t_tot), "p95": q(t_tot, 95), "max": max(t_tot)},
       "equipo": f"{platform.processor()} | Python {platform.python_version()} | numpy {np.__version__}"}
json.dump(res, open("bench_latencia.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
