"""Pruebas del reconocedor de señas.

Incluye una comparación cuantitativa contra el método de la versión 1
(similitud coseno sobre las coordenadas crudas) bajo perturbaciones que imitan
lo que ocurre en la práctica: el niño se acerca o se aleja de la cámara, inclina
la muñeca y nunca repite la seña exactamente igual.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from handsingkids.vision.classifier import GestureClassifier  # noqa: E402
from handsingkids.vision.features import pose_features  # noqa: E402
from handsingkids.vision.templates import TemplateStore  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "calibracion_v1.json"


# ------------------------------------------------------------ utilidades

def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def perturb(hands: list[dict], rng: np.random.Generator, *,
            noise: float = 0.0, scale: float = 1.0,
            rotation_deg: float | None = None,
            independent: bool = True) -> list[dict]:
    """Aplica ruido, cambio de escala y giro en el plano de la imagen.

    Con `independent=True` cada mano recibe su propio giro, que es lo que
    ocurre de verdad: las dos muñecas de un niño no se inclinan a la vez."""
    out = []
    for h in hands:
        ang = (rotation_deg if rotation_deg is not None
               else float(rng.uniform(-18, 18)))
        if not independent and rotation_deg is None:
            ang = 0.0
        theta = np.deg2rad(ang)
        c, sn = np.cos(theta), np.sin(theta)
        rot = np.array([[c, -sn], [sn, c]])
        pts = np.asarray(h["landmarks"], dtype=float).copy()
        ref = float(np.linalg.norm(pts[9] - pts[0])) or 1e-6
        pts = pts * scale
        pts[:, :2] = pts[:, :2] @ rot.T
        if noise:
            pts = pts + rng.normal(0.0, noise * ref, size=pts.shape)
        out.append({"landmarks": pts.tolist(), "hand_label": h["hand_label"]})
    return out


def transition(a: list[dict], b: list[dict], t: float = 0.5) -> list[dict]:
    """Postura intermedia entre dos señas: lo que la cámara ve mientras las
    manos viajan de una a otra. Lo correcto es no reconocer nada."""
    by_label = {h["hand_label"]: h for h in b}
    out = []
    for h in a:
        other = by_label.get(h["hand_label"])
        if other is None:
            out.append(h)
            continue
        pa = np.asarray(h["landmarks"], dtype=float)
        pb = np.asarray(other["landmarks"], dtype=float)
        out.append({"landmarks": ((1 - t) * pa + t * pb).tolist(),
                    "hand_label": h["hand_label"]})
    return out


def chimera(a: list[dict], b: list[dict]) -> list[dict]:
    """Mano izquierda de una seña y derecha de otra: no es ninguna nota."""
    left = [h for h in a if h["hand_label"] == "Left"]
    right = [h for h in b if h["hand_label"] == "Right"]
    return left + right


def v1_vector(hands: list[dict]) -> np.ndarray:
    """Reproduce el vector de la versión 1: coordenadas crudas concatenadas."""
    vec: list[float] = []
    for h in sorted(hands, key=lambda x: x["hand_label"]):
        for lm in h["landmarks"]:
            vec.extend(lm)
    return np.asarray(vec, dtype=float)


def v1_classify(vec: np.ndarray, templates: dict[str, np.ndarray],
                threshold: float = 0.65) -> str | None:
    best, best_sim = None, -1.0
    for code, tpl in templates.items():
        na, nb = np.linalg.norm(vec), np.linalg.norm(tpl)
        if na == 0 or nb == 0:
            continue
        sim = float(np.dot(vec, tpl) / (na * nb))
        if sim > best_sim:
            best, best_sim = code, sim
    return best if best_sim >= threshold else None


# ------------------------------------------------------------- pruebas

def test_identidad() -> None:
    """Cada seña calibrada debe reconocerse a sí misma."""
    raw = load_fixture()
    store = TemplateStore(0)
    for code, entry in raw.items():
        store.add_sample(code, entry["hands"])
    clf = GestureClassifier(store)
    clf.calibrate_temperature()
    for code, entry in raw.items():
        pred = clf.classify(pose_features(entry["hands"]))
        assert pred.note == code, f"{code} se reconoció como {pred.note}"


def test_invariancia_escala_y_giro() -> None:
    """Acercarse a la cámara o inclinar la muñeca no debe cambiar la lectura."""
    raw = load_fixture()
    store = TemplateStore(0)
    for code, entry in raw.items():
        store.add_sample(code, entry["hands"])
    clf = GestureClassifier(store)
    clf.calibrate_temperature()
    rng = np.random.default_rng(7)
    fallos = []
    for code, entry in raw.items():
        for scale in (0.75, 1.0, 1.35):
            for rot in (-15.0, 0.0, 15.0):
                h = perturb(entry["hands"], rng, scale=scale, rotation_deg=rot)
                pred = clf.classify(pose_features(h))
                if pred.note != code:
                    fallos.append((code, scale, rot, pred.note))
    assert not fallos, f"fallos con escala/giro: {fallos}"


def _setup():
    raw = load_fixture()
    store = TemplateStore(0)
    for code, entry in raw.items():
        store.add_sample(code, entry["hands"])
    clf = GestureClassifier(store)
    clf.calibrate_temperature()
    v1_templates = {c: v1_vector(e["hands"]) for c, e in raw.items()}
    return raw, clf, v1_templates


def benchmark_aciertos(noise_levels=(0.0, 0.03, 0.06, 0.09),
                       repeticiones: int = 60, seed: int = 11) -> list[dict]:
    """Señas válidas repetidas con variación: ¿se reconoce la nota correcta?"""
    raw, clf, v1_templates = _setup()
    rng = np.random.default_rng(seed)
    filas = []
    for noise in noise_levels:
        nuevo_ok = v1_ok = total = 0
        for code, entry in raw.items():
            for _ in range(repeticiones):
                h = perturb(entry["hands"], rng, noise=noise,
                            scale=float(rng.uniform(0.8, 1.25)))
                total += 1
                nuevo_ok += (clf.classify(pose_features(h)).note == code)
                v1_ok += (v1_classify(v1_vector(h), v1_templates) == code)
        filas.append({"ruido": noise, "n": total,
                      "nuevo": 100.0 * nuevo_ok / total,
                      "v1": 100.0 * v1_ok / total})
    return filas


def benchmark_falsos_positivos(repeticiones: int = 40, seed: int = 23) -> dict:
    """Posturas que no son ninguna seña: transiciones entre dos notas y manos
    cruzadas. Lo correcto es no reconocer nada; cada nota emitida es un falso
    positivo que, dentro del juego, se traduce en una nota tocada sin querer."""
    raw, clf, v1_templates = _setup()
    rng = np.random.default_rng(seed)
    codes = list(raw)
    nuevo_fp = v1_fp = total = 0
    for _ in range(repeticiones):
        for i, a in enumerate(codes):
            b = codes[(i + 3) % len(codes)]
            for pose in (transition(raw[a]["hands"], raw[b]["hands"], 0.5),
                         chimera(raw[a]["hands"], raw[b]["hands"])):
                pose = perturb(pose, rng, noise=0.02,
                               scale=float(rng.uniform(0.9, 1.15)))
                total += 1
                nuevo_fp += clf.classify(pose_features(pose)).note is not None
                v1_fp += v1_classify(v1_vector(pose), v1_templates) is not None
    return {"n": total,
            "nuevo": 100.0 * nuevo_fp / total,
            "v1": 100.0 * v1_fp / total}


def test_rechaza_posturas_intermedias() -> None:
    fp = benchmark_falsos_positivos(repeticiones=10)
    assert fp["nuevo"] < 25.0, fp
    assert fp["nuevo"] < fp["v1"], fp


def test_acierta_con_variacion() -> None:
    filas = benchmark_aciertos(noise_levels=(0.0, 0.06), repeticiones=25)
    assert filas[0]["nuevo"] >= 95.0, filas[0]
    assert filas[-1]["nuevo"] >= 80.0, filas[-1]


if __name__ == "__main__":
    test_identidad()
    test_invariancia_escala_y_giro()
    print("A. SEÑAS VÁLIDAS con variación de tamaño, giro por mano y ruido")
    print("   ruido   método nuevo   método v1")
    for f in benchmark_aciertos():
        print(f"   {f['ruido']:5.2f}   {f['nuevo']:11.1f}%   {f['v1']:8.1f}%")
    fp = benchmark_falsos_positivos()
    print()
    print("B. POSTURAS QUE NO SON NINGUNA SEÑA (transiciones y manos cruzadas)")
    print(f"   n = {fp['n']}   notas disparadas por error:")
    print(f"   método nuevo: {fp['nuevo']:.1f}%     método v1: {fp['v1']:.1f}%")
    print("\nTodas las pruebas pasaron.")
