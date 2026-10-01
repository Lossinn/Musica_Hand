"""Descriptor invariante de una postura de manos.

Motivación: la versión 1 comparaba directamente el vector de 126 coordenadas
mediante similitud coseno. Ese esquema hereda toda la variabilidad de la escena
—distancia del niño a la cámara, inclinación de la muñeca, tamaño de la mano—
y además produce similitudes altas entre señas distintas, porque dos nubes de
puntos con forma de mano siempre se parecen.

Aquí la postura se describe con magnitudes geométricas que no cambian cuando el
niño se acerca, se aleja o gira un poco la muñeca:

    - curvatura de cada dedo (razón entre la distancia punta-nudillo y la suma
      de las falanges),
    - apertura entre dedos contiguos,
    - distancia del pulgar a cada yema,
    - normal del plano de la palma,
    - dirección de la mano en el plano de la imagen,
    - forma de la mano tras normalizar escala y rotación,
    - geometría relativa entre las dos manos.

Cada bloque se compara por separado y con su propio peso, de modo que los 40
números de la forma no aplasten a los 5 de la curvatura.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

WRIST = 0
FINGERS = {                      # nudillo -> yema
    "pulgar": (1, 2, 3, 4),
    "indice": (5, 6, 7, 8),
    "medio": (9, 10, 11, 12),
    "anular": (13, 14, 15, 16),
    "menique": (17, 18, 19, 20),
}
FINGER_ORDER = ("pulgar", "indice", "medio", "anular", "menique")
MIDDLE_MCP = 9
INDEX_MCP = 5
PINKY_MCP = 17

# Tamaño de cada bloque dentro del vector de una mano.
BLOCKS: tuple[tuple[str, int], ...] = (
    ("curvatura", 5),
    ("apertura", 4),
    ("pulgar_yemas", 4),
    ("normal_palma", 3),
    ("direccion", 2),
    ("forma", 40),
)
HAND_DIM = sum(size for _, size in BLOCKS)          # 58
RELATIONAL_DIM = 4
BLOCK_WEIGHTS = {
    "curvatura": 3.0,
    "apertura": 1.2,
    "pulgar_yemas": 2.0,
    "normal_palma": 1.4,
    "direccion": 2.0,
    "forma": 2.6,
    "relacional": 1.6,
}


def _as_array(landmarks) -> np.ndarray:
    a = np.asarray(landmarks, dtype=np.float64)
    if a.shape != (21, 3):
        raise ValueError(f"Se esperaban 21 puntos de 3 coordenadas, llegó {a.shape}")
    return a


def _unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-9 else np.zeros_like(v)


def hand_scale(pts: np.ndarray) -> float:
    """Tamaño de referencia de la mano: muñeca al nudillo del dedo medio."""
    s = float(np.linalg.norm(pts[MIDDLE_MCP] - pts[WRIST]))
    return s if s > 1e-6 else 1e-6


def _curls(pts: np.ndarray, scale: float) -> np.ndarray:
    out = []
    for name in FINGER_ORDER:
        a, b, c, d = FINGERS[name]
        chain = (np.linalg.norm(pts[b] - pts[a])
                 + np.linalg.norm(pts[c] - pts[b])
                 + np.linalg.norm(pts[d] - pts[c]))
        direct = np.linalg.norm(pts[d] - pts[a])
        ratio = direct / chain if chain > 1e-9 else 0.0
        # Un dedo extendido da ~1.0; uno completamente doblado, ~0.35.
        out.append(float(np.clip((ratio - 0.35) / 0.65, 0.0, 1.0)))
    return np.array(out)


def _spreads(pts: np.ndarray) -> np.ndarray:
    """Ángulo entre dedos contiguos, normalizado a [0, 1]."""
    dirs = []
    for name in FINGER_ORDER:
        a, _, _, d = FINGERS[name]
        dirs.append(_unit(pts[d] - pts[a]))
    out = []
    for i in range(4):
        cos = float(np.clip(np.dot(dirs[i], dirs[i + 1]), -1.0, 1.0))
        out.append(float(np.arccos(cos) / np.pi))
    return np.array(out)


def _thumb_to_tips(pts: np.ndarray, scale: float) -> np.ndarray:
    thumb = pts[FINGERS["pulgar"][3]]
    out = []
    for name in ("indice", "medio", "anular", "menique"):
        tip = pts[FINGERS[name][3]]
        out.append(float(np.clip(np.linalg.norm(tip - thumb) / scale, 0.0, 3.0)) / 3.0)
    return np.array(out)


def palm_normal(pts: np.ndarray) -> np.ndarray:
    """Normal del plano de la palma; distingue palma arriba, abajo o de canto."""
    v1 = pts[INDEX_MCP] - pts[WRIST]
    v2 = pts[PINKY_MCP] - pts[WRIST]
    return _unit(np.cross(v1, v2))


def hand_direction(pts: np.ndarray) -> np.ndarray:
    """Dirección muñeca -> nudillo medio en el plano de la imagen."""
    v = pts[MIDDLE_MCP][:2] - pts[WRIST][:2]
    return _unit(v)


def _shape(pts: np.ndarray, scale: float, direction: np.ndarray) -> np.ndarray:
    """Coordenadas 2D tras llevar la muñeca al origen, normalizar el tamaño y
    girar la mano hasta que apunte hacia arriba. Se omite la muñeca, que
    siempre queda en (0, 0)."""
    xy = (pts[:, :2] - pts[WRIST, :2]) / scale
    theta = float(np.arctan2(direction[1], direction[0]))
    alpha = (-np.pi / 2.0) - theta
    c, s = np.cos(alpha), np.sin(alpha)
    rot = np.array([[c, -s], [s, c]])
    rotated = xy @ rot.T
    return rotated[1:].reshape(-1)      # 20 puntos x 2 = 40


def hand_features(landmarks) -> np.ndarray:
    """Vector de 58 números que describe una mano."""
    pts = _as_array(landmarks)
    pts = pts - pts[WRIST]
    scale = hand_scale(pts)
    direction = hand_direction(pts)
    return np.concatenate([
        _curls(pts, scale),
        _spreads(pts),
        _thumb_to_tips(pts, scale),
        palm_normal(pts),
        direction,
        _shape(pts, scale, direction),
    ])


def _relational(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Geometría entre las dos manos: una encima de otra, juntas, separadas."""
    lp = _as_array(left)
    rp = _as_array(right)
    scale = 0.5 * (hand_scale(lp - lp[WRIST]) + hand_scale(rp - rp[WRIST]))
    offset = (rp[WRIST][:2] - lp[WRIST][:2]) / max(scale, 1e-6)
    offset = np.clip(offset, -6.0, 6.0) / 6.0
    dist = float(np.clip(np.linalg.norm(rp[WRIST] - lp[WRIST]) / max(scale, 1e-6),
                         0.0, 8.0)) / 8.0
    dl = hand_direction(lp - lp[WRIST])
    dr = hand_direction(rp - rp[WRIST])
    align = float(np.clip(np.dot(dl, dr), -1.0, 1.0))
    return np.array([offset[0], offset[1], dist, align])


@dataclass(frozen=True)
class PoseFeatures:
    """Descriptor completo de una postura, con los bloques identificados para
    poder pesarlos al comparar."""
    vector: np.ndarray
    hands: int              # 1 o 2
    labels: tuple[str, ...]
    relational_valid: bool = True
    """False cuando las manos vienen ya centradas en su propia muñeca y, por
    tanto, la posición de una respecto a la otra se perdió. Es el caso de las
    calibraciones de la versión 1."""

    @property
    def dim(self) -> int:
        return int(self.vector.size)


def _ordered(hands_data: list[dict]) -> list[dict]:
    """Orden estable: primero la mano izquierda. La etiqueta la entrega
    MediaPipe; como la calibración y el juego usan la misma convención, el
    orden es consistente aunque la imagen esté en modo espejo."""
    return sorted(hands_data, key=lambda h: str(h.get("hand_label", "")))


def pose_features(hands_data: list[dict]) -> PoseFeatures | None:
    """Construye el descriptor a partir de la salida del detector.

    `hands_data` es una lista de diccionarios con las claves `landmarks`
    (21 x 3) y `hand_label` ('Left' o 'Right')."""
    if not hands_data:
        return None
    ordered = _ordered(hands_data)[:2]
    parts = [hand_features(h["landmarks"]) for h in ordered]
    labels = tuple(str(h.get("hand_label", "?")) for h in ordered)
    relational_valid = True
    if len(ordered) == 2:
        parts.append(_relational(ordered[0]["landmarks"], ordered[1]["landmarks"]))
        wrists = [_as_array(h["landmarks"])[WRIST] for h in ordered]
        # Si ambas muñecas están en el origen, las manos llegaron ya centradas
        # y la geometría relativa entre ellas no aporta información.
        relational_valid = bool(np.linalg.norm(wrists[0] - wrists[1]) > 1e-6)
    return PoseFeatures(vector=np.concatenate(parts), hands=len(ordered),
                        labels=labels, relational_valid=relational_valid)


# ------------------------------------------------------- distancia ponderada

def _block_slices(hands: int) -> list[tuple[str, slice]]:
    slices: list[tuple[str, slice]] = []
    offset = 0
    for _ in range(hands):
        for name, size in BLOCKS:
            slices.append((name, slice(offset, offset + size)))
            offset += size
    if hands == 2:
        slices.append(("relacional", slice(offset, offset + RELATIONAL_DIM)))
    return slices


_SLICE_CACHE: dict[int, list[tuple[str, slice]]] = {}


def weighted_distance(a: np.ndarray, b: np.ndarray, hands: int,
                      use_relational: bool = True) -> float:
    """Distancia entre dos descriptores.

    Cada bloque aporta el promedio de sus diferencias al cuadrado multiplicado
    por su peso, de modo que la contribución no dependa del número de
    dimensiones del bloque:

        d^2 = sum_g  w_g * (1/|g|) * sum_{i in g} (a_i - b_i)^2
    """
    if a.shape != b.shape:
        return float("inf")
    if hands not in _SLICE_CACHE:
        _SLICE_CACHE[hands] = _block_slices(hands)
    total = 0.0
    weight_sum = 0.0
    for name, sl in _SLICE_CACHE[hands]:
        if name == "relacional" and not use_relational:
            continue
        w = BLOCK_WEIGHTS[name]
        diff = a[sl] - b[sl]
        total += w * float(np.dot(diff, diff)) / max(1, diff.size)
        weight_sum += w
    return float(np.sqrt(total / weight_sum)) if weight_sum else float("inf")
