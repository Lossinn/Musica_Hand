"""Almacén de plantillas de señas por perfil.

Cada nota guarda varias muestras —no una sola— porque un niño nunca repite la
seña exactamente igual. Se conserva además la postura cruda de una de ellas
para poder dibujar en pantalla la seña que debe imitar.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from ..core.config import legacy_templates_path, templates_path
from ..domain.notes import NOTE_CODES
from .features import pose_features, weighted_distance

FORMAT_VERSION = 2
SAMPLES_PER_NOTE = 3


class TemplateStore:
    """Colección de descriptores por nota, con serialización a disco."""

    def __init__(self, profile_id: int) -> None:
        self.profile_id = profile_id
        self.path: Path = templates_path(profile_id)
        self.hands: int = 2
        self.relational: bool = True
        """Si es False, las muestras no conservan la posición de una mano
        respecto a la otra y ese bloque se ignora al comparar."""
        self.samples: dict[str, list[np.ndarray]] = {}
        self.poses: dict[str, list[list[dict]]] = {}
        self.created_at: float = 0.0

    # ------------------------------------------------------------ estado
    @property
    def notes(self) -> list[str]:
        return [c for c in NOTE_CODES if self.samples.get(c)]

    @property
    def is_complete(self) -> bool:
        return len(self.notes) == len(NOTE_CODES)

    def count(self, note: str) -> int:
        return len(self.samples.get(note, []))

    def clear(self) -> None:
        self.samples.clear()
        self.poses.clear()

    # --------------------------------------------------------- captura
    def add_sample(self, note: str, hands_data: list[dict]) -> bool:
        """Registra una muestra. Devuelve False si la postura no es utilizable."""
        pf = pose_features(hands_data)
        if pf is None:
            return False
        if self.samples and pf.hands != self.hands:
            return False
        self.hands = pf.hands
        self.relational = self.relational and pf.relational_valid
        self.samples.setdefault(note, []).append(pf.vector)
        self.poses.setdefault(note, []).append(
            [{"landmarks": [list(map(float, p)) for p in h["landmarks"]],
              "hand_label": h.get("hand_label", "?")} for h in hands_data])
        # Se conservan solo las últimas muestras para que el archivo no crezca.
        self.samples[note] = self.samples[note][-SAMPLES_PER_NOTE:]
        self.poses[note] = self.poses[note][-SAMPLES_PER_NOTE:]
        return True

    def drop(self, note: str) -> None:
        self.samples.pop(note, None)
        self.poses.pop(note, None)

    def pose_for(self, note: str) -> list[dict] | None:
        poses = self.poses.get(note)
        return poses[-1] if poses else None

    # -------------------------------------------------------- diagnóstico
    def separation(self) -> list[tuple[str, str, float]]:
        """Pares de notas ordenados de más parecido a más distinto.

        Sirve para avisar durante la calibración cuando dos señas quedaron
        demasiado parecidas y la aplicación las va a confundir."""
        pairs: list[tuple[str, str, float]] = []
        codes = self.notes
        for i, a in enumerate(codes):
            for b in codes[i + 1:]:
                d = min(weighted_distance(x, y, self.hands, self.relational)
                        for x in self.samples[a] for y in self.samples[b])
                pairs.append((a, b, d))
        pairs.sort(key=lambda t: t[2])
        return pairs

    def spread(self, note: str) -> float:
        """Dispersión interna de las muestras de una nota."""
        s = self.samples.get(note, [])
        if len(s) < 2:
            return 0.0
        return max(weighted_distance(s[i], s[j], self.hands, self.relational)
                   for i in range(len(s)) for j in range(i + 1, len(s)))

    # ------------------------------------------------------ persistencia
    def to_dict(self) -> dict:
        return {
            "version": FORMAT_VERSION,
            "profile_id": self.profile_id,
            "created_at": self.created_at or time.time(),
            "saved_at": time.time(),
            "hands": self.hands,
            "relational": self.relational,
            "notes": {
                code: {
                    "samples": [list(map(float, v)) for v in self.samples[code]],
                    "poses": self.poses.get(code, []),
                }
                for code in self.samples
            },
        }

    def save(self) -> Path:
        if not self.created_at:
            self.created_at = time.time()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.to_dict(), ensure_ascii=False),
                             encoding="utf-8")
        return self.path

    def load(self) -> bool:
        if not self.path.exists():
            return False
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return False
        return self._absorb(data)

    def _absorb(self, data: dict) -> bool:
        if data.get("version") != FORMAT_VERSION:
            return False
        self.hands = int(data.get("hands", 2))
        self.relational = bool(data.get("relational", True))
        self.created_at = float(data.get("created_at", 0.0))
        self.samples = {}
        self.poses = {}
        for code, entry in (data.get("notes") or {}).items():
            samples = [np.asarray(v, dtype=np.float64)
                       for v in entry.get("samples", [])]
            if samples:
                self.samples[code] = samples
                self.poses[code] = entry.get("poses", [])
        return bool(self.samples)

    # ----------------------------------------------------- importación v1
    def import_legacy(self, path: Path | str | None = None) -> int:
        """Convierte un `pentagrama_calibrado.json` de la versión 1.

        Aquel formato guardaba una sola postura por nota; se recalcula su
        descriptor y se usa como primera muestra, de modo que una calibración
        vieja sigue sirviendo sin repetir el proceso."""
        p = Path(path) if path else legacy_templates_path()
        if not p.exists():
            return 0
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return 0
        imported = 0
        self.relational = True
        for code, entry in raw.items():
            hands = entry.get("hands") if isinstance(entry, dict) else None
            if not hands:
                continue
            if self.add_sample(code, hands):
                imported += 1
        if imported:
            self.created_at = time.time()
        return imported


def load_or_import(profile_id: int) -> TemplateStore:
    """Carga las plantillas del perfil; si no existen, intenta traer las de la
    versión 1 que estén junto al proyecto."""
    store = TemplateStore(profile_id)
    if store.load():
        return store
    if store.import_legacy():
        store.save()
    return store
