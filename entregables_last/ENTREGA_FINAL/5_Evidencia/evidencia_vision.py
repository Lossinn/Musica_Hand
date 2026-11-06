"""Evidencia reproducible de la capa de visión (Corte 3).

Reutiliza las funciones de tests/test_vision.py sin modificarlas. Produce:
  - tasas con intervalo de Wilson al 95 %,
  - desglose de falsos positivos (transición vs. manos cruzadas),
  - robustez del 8 % frente a la semilla (30 semillas),
  - matrices 8x8: coseno de la v1 y distancia del descriptor actual,
  - latencia por fotograma (descriptor + clasificador).
Salida: resultados_vision.json y matriz_similitud.csv / .png en esta carpeta.

Uso (desde cualquier carpeta):  python -I evidencia_vision.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1] / "03_Codigo" / "HandSingKids7"
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))

import test_vision as tv  # noqa: E402
from handsingkids.vision.features import pose_features, weighted_distance  # noqa: E402


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    mitad = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (centro - mitad), 100 * (centro + mitad)


def fila(nombre: str, k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"nombre": nombre, "k": k, "n": n, "pct": 100 * k / n,
            "ic95_lo": lo, "ic95_hi": hi}


def aciertos_por_ruido() -> list[dict]:
    out = []
    for f in tv.benchmark_aciertos():            # semilla 11, 60 repeticiones
        n = f["n"]
        out.append({"ruido": f["ruido"], "n": n,
                    "nuevo": fila("nuevo", round(f["nuevo"] * n / 100), n),
                    "v1": fila("v1", round(f["v1"] * n / 100), n)})
    return out


def falsos_positivos() -> dict:
    """Misma construcción que benchmark_falsos_positivos, con desglose."""
    raw, clf, v1t = tv._setup()
    rng = np.random.default_rng(23)
    codes = list(raw)
    cont = {"transicion": [0, 0, 0], "manos_cruzadas": [0, 0, 0]}  # n, nuevo, v1
    for _ in range(40):
        for i, a in enumerate(codes):
            b = codes[(i + 3) % len(codes)]
            poses = (("transicion", tv.transition(raw[a]["hands"], raw[b]["hands"], 0.5)),
                     ("manos_cruzadas", tv.chimera(raw[a]["hands"], raw[b]["hands"])))
            for tipo, pose in poses:
                pose = tv.perturb(pose, rng, noise=0.02,
                                  scale=float(rng.uniform(0.9, 1.15)))
                cont[tipo][0] += 1
                cont[tipo][1] += clf.classify(pose_features(pose)).note is not None
                cont[tipo][2] += tv.v1_classify(tv.v1_vector(pose), v1t) is not None
    n = sum(c[0] for c in cont.values())
    kn = sum(c[1] for c in cont.values())
    kv = sum(c[2] for c in cont.values())
    return {"global_nuevo": fila("nuevo", kn, n), "global_v1": fila("v1", kv, n),
            "por_tipo": {t: {"nuevo": fila("nuevo", c[1], c[0]),
                             "v1": fila("v1", c[2], c[0])} for t, c in cont.items()}}


def robustez_semillas(n_semillas: int = 30) -> dict:
    tasas = []
    for s in range(100, 100 + n_semillas):
        r = tv.benchmark_falsos_positivos(repeticiones=40, seed=s)
        tasas.append(r["nuevo"])
    a = np.array(tasas)
    return {"semillas": n_semillas, "media": float(a.mean()), "sd": float(a.std(ddof=1)),
            "min": float(a.min()), "max": float(a.max())}


def matrices() -> dict:
    raw, clf, _ = tv._setup()
    codes = list(raw)
    v1v = {c: tv.v1_vector(raw[c]["hands"]) for c in codes}
    feats = {c: pose_features(raw[c]["hands"]) for c in codes}
    cos = np.zeros((8, 8))
    dist = np.zeros((8, 8))
    for i, a in enumerate(codes):
        for j, b in enumerate(codes):
            va, vb = v1v[a], v1v[b]
            cos[i, j] = float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb)))
            fa, fb = feats[a], feats[b]
            dist[i, j] = weighted_distance(fa.vector, fb.vector, fa.hands,
                                           clf.store.relational and fa.relational_valid)
    iu = [(i, j) for i in range(8) for j in range(8) if i != j]
    sobre = [(codes[i], codes[j], cos[i, j]) for i, j in iu if cos[i, j] >= 0.65]
    pico = max(iu, key=lambda p: cos[p])
    d_min = min(dist[i, j] for i, j in iu)
    return {"codes": codes, "cos": cos.tolist(), "dist": dist.tolist(),
            "pares_ordenados": len(iu), "pares_sobre_0_65": len(sobre),
            "pares_unicos_sobre_0_65": len(sobre) // 2,
            "max_cos": [codes[pico[0]], codes[pico[1]], float(cos[pico])],
            "dist_min_entre_notas": float(d_min),
            "temperatura": float(clf.temperature),
            "dist_max_entre_notas": float(max(dist[i, j] for i, j in iu))}


def latencia(reps: int = 2000) -> dict:
    raw, clf, _ = tv._setup()
    hands = raw[list(raw)[0]]["hands"]
    for _ in range(100):
        clf.classify(pose_features(hands))
    t = []
    for _ in range(reps):
        t0 = time.perf_counter()
        clf.classify(pose_features(hands))
        t.append((time.perf_counter() - t0) * 1000)
    a = np.array(t)
    return {"reps": reps, "media_ms": float(a.mean()), "p95_ms": float(np.percentile(a, 95)),
            "max_ms": float(a.max())}


def figura(m: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 4.2))
    for a, mat, tit, fmt, cm in (
            (ax[0], np.array(m["cos"]), "(a) Similitud coseno, método v1", "{:.2f}", "Reds"),
            (ax[1], np.array(m["dist"]), "(b) Distancia por bloques, descriptor actual", "{:.2f}", "Blues_r")):
        im = a.imshow(mat, cmap=cm)
        a.set_xticks(range(8)); a.set_yticks(range(8))
        a.set_xticklabels(m["codes"], rotation=45, fontsize=8)
        a.set_yticklabels(m["codes"], fontsize=8)
        a.set_title(tit, fontsize=9)
        for i in range(8):
            for j in range(8):
                a.text(j, i, fmt.format(mat[i, j]), ha="center", va="center", fontsize=6.5,
                       color="white" if im.norm(mat[i, j]) > 0.6 else "black")
        fig.colorbar(im, ax=a, fraction=0.046)
    fig.tight_layout()
    fig.savefig(AQUI / "matriz_similitud.png", dpi=300)
    fig.savefig(AQUI / "matriz_similitud.svg")


def main() -> None:
    m = matrices()
    res = {"aciertos": aciertos_por_ruido(), "falsos_positivos": falsos_positivos(),
           "robustez_fp_nuevo": robustez_semillas(), "matrices": m, "latencia": latencia()}
    (AQUI / "resultados_vision.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(AQUI / "matriz_similitud.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cos_v1"] + m["codes"])
        for c, r in zip(m["codes"], m["cos"]):
            w.writerow([c] + [f"{x:.4f}" for x in r])
        w.writerow([])
        w.writerow(["dist_actual"] + m["codes"])
        for c, r in zip(m["codes"], m["dist"]):
            w.writerow([c] + [f"{x:.4f}" for x in r])
    figura(m)
    print(json.dumps(res, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
