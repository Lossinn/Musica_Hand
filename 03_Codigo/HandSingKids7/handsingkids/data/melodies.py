"""Melodías que un niño grabó en Modo Libre: almacenamiento en JSON, un
archivo por melodía.

No viven en la base de datos porque no son parte del catálogo pedagógico:
son la composición propia del niño, no algo que el optimizador o el Agente
Adaptativo deban conocer. Guardarlas como archivos sueltos en `melodias/`
también hace trivial que una familia los copie, los respalde o los borre a
mano, tal como ya decía el README antes de este módulo.

Desde la versión 6, además de la lista de notas y la duración total, se
guarda el intervalo real (en milisegundos) entre cada nota y la anterior.
Es lo que permite que el módulo "Canciones" reproduzca una melodía grabada
"a mi ritmo" de verdad, en vez de repartir la duración total en partes
iguales. Los archivos guardados antes de este cambio no tienen ese campo:
se reconstruye un promedio razonable a partir de la duración total, así
que siguen abriendo y reproduciéndose sin problema.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from ..core.config import data_dir
from ..domain.notes import SILENCE

CARPETA = "melodias"


@dataclass
class RecordedMelody:
    path: Path
    profile_name: str
    notes: list[str]
    duration_s: float
    created_at: float
    gaps_ms: list[float] = field(default_factory=list)

    @property
    def note_count(self) -> int:
        return sum(1 for c in self.notes if c != SILENCE)

    @property
    def silence_count(self) -> int:
        return sum(1 for c in self.notes if c == SILENCE)


def folder() -> Path:
    p = data_dir() / CARPETA
    p.mkdir(parents=True, exist_ok=True)
    return p


def save(profile_name: str, notes: list[str], duration_s: float,
        gaps_ms: list[float] | None = None) -> Path:
    """Guarda una melodía nueva y devuelve la ruta del archivo creado."""
    nombre = f"{profile_name}_{int(time.time())}.json"
    ruta = folder() / nombre
    payload: dict = {
        "perfil": profile_name,
        "notas": list(notes),
        "duracion_seg": round(duration_s, 1),
        "creada": time.time(),
    }
    if gaps_ms:
        payload["gaps_ms"] = [round(float(g), 1) for g in gaps_ms]
    ruta.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    return ruta


def list_for_profile(profile_name: str) -> list[RecordedMelody]:
    """Melodías del niño indicado, más recientes primero."""
    out: list[RecordedMelody] = []
    for ruta in folder().glob("*.json"):
        try:
            data = json.loads(ruta.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("perfil") != profile_name:
            continue
        out.append(RecordedMelody(
            path=ruta, profile_name=profile_name,
            notes=[str(c) for c in data.get("notas", [])],
            duration_s=float(data.get("duracion_seg", 0.0) or 0.0),
            created_at=float(data.get("creada", ruta.stat().st_mtime)),
            gaps_ms=[float(g) for g in data.get("gaps_ms", [])]))
    out.sort(key=lambda m: m.created_at, reverse=True)
    return out


def estimated_gaps_ms(m: RecordedMelody) -> list[float]:
    """Los intervalos reales si se grabaron con la melodía, o un promedio a
    partir de la duración total si es de antes de que se guardaran."""
    n = len(m.notes)
    if m.gaps_ms and len(m.gaps_ms) >= n:
        return m.gaps_ms[:n]
    if n <= 1 or m.duration_s <= 0:
        return [0.0] * n
    promedio = (m.duration_s * 1000.0) / n
    return [promedio] * n


def delete(m: RecordedMelody) -> None:
    try:
        m.path.unlink(missing_ok=True)
    except Exception:
        pass
