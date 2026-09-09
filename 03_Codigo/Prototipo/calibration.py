"""Calibración de las señas del niño (Fases 3–4). IMPLEMENTADO (captura manual).

Heredado de la versión anterior (MusicaManos): cada nota es una **seña de dos
manos** que el niño calibra una vez. La plantilla es la lista de landmarks de
ambas manos, centrados en la muñeca.

    Antes:  ubicaciones definidas a mano -> configuración -> reconocimiento
    Ahora:  el niño hace la seña -> se captura -> se guarda -> se reconoce

Formato en disco (data/calibration/<user_id>.json), idéntico al
`pentagrama_calibrado.reference.json` de la versión anterior:

    {
      "SOL3": {"hands": [{"landmarks": [[x,y,z]·21], "hand_label": "Left"},
                         {"landmarks": [[x,y,z]·21], "hand_label": "Right"}]},
      ...
    }

Fase 4 (pendiente): reemplazar la captura manual por detección automática de
pose estable y normalización por escala de la mano — sin cambiar este formato.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import config
from .recognizer import GestureRecognizer, hands_to_vector


@dataclass
class CalibrationProfile:
    """Configuración calibrada `C`. Serializable a/desde JSON."""

    user_id: str
    # referencia por nota: snapshot de las dos manos (wrist-relative)
    references: dict[str, dict] = field(default_factory=dict)
    hand_scale: float = 1.0
    created_at: str = ""
    version: int = 2                      # v2 = señas de dos manos

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "CalibrationProfile":
        data = json.loads(text)
        # Compatibilidad: el JSON de la versión anterior es {nota: {"hands": [...]}}
        # sin envoltura. Se detecta por la ausencia de "references".
        if "references" not in data and "user_id" not in data:
            return cls(user_id="referencia", references=data)
        return cls(**data)


class Calibrator:
    """Captura, guarda y sirve las plantillas de seña de un niño.

    Uso guiado (una nota a la vez):
        cal = Calibrator(user_id="nino_01")
        cal.iniciar()
        while not cal.completa():
            nota = cal.siguiente_nota()
            # ... el niño hace la seña, vision.detect() -> hands_data ...
            cal.capturar(nota, hands_data)
        cal.save()

    En juego:
        cal.load()
        templates = cal.templates()        # {nota: vector 126}
    """

    def __init__(self, user_id: str = "default", notas: tuple[str, ...] | None = None) -> None:
        self.user_id = user_id
        self.notas = notas or config.NOTAS
        self.profile: CalibrationProfile | None = None
        self._idx = 0                       # puntero de calibración guiada
        self._templates_cache: dict[str, np.ndarray] | None = None

    # ── calibración guiada ──────────────────────────────────────────────
    def iniciar(self) -> None:
        """Empieza de cero: perfil vacío, puntero en la primera nota."""
        self.profile = CalibrationProfile(
            user_id=self.user_id, created_at=_now_iso()
        )
        self._idx = 0
        self._templates_cache = None

    def siguiente_nota(self) -> str | None:
        """Nota que toca calibrar ahora, o None si ya están todas."""
        if self._idx >= len(self.notas):
            return None
        return self.notas[self._idx]

    def capturar(self, nota: str, hands_data: list[dict]) -> bool:
        """Guarda la seña de dos manos para `nota`. Devuelve False (y no avanza)
        si no se ven exactamente dos manos."""
        if self.profile is None:
            self.iniciar()
        assert self.profile is not None

        if not hands_data or len(hands_data) < config.HANDS_PER_GESTURE:
            return False

        self.profile.references[nota] = {
            "hands": [
                {"landmarks": _as_list(h["landmarks"]), "hand_label": h.get("hand_label", "")}
                for h in sorted(hands_data, key=lambda h: h.get("hand_label", ""))[:config.HANDS_PER_GESTURE]
            ]
        }
        self._templates_cache = None
        if nota == self.siguiente_nota():
            self._idx += 1
        return True

    def recapturar(self, nota: str) -> None:
        """Marca una nota para volver a calibrarla (borra su plantilla)."""
        if self.profile and nota in self.profile.references:
            del self.profile.references[nota]
            self._templates_cache = None

    # ── estado ─────────────────────────────────────────────────────────
    def notas_calibradas(self) -> list[str]:
        return list(self.profile.references) if self.profile else []

    def completa(self) -> bool:
        return set(self.notas) <= set(self.notas_calibradas())

    def progreso(self) -> float:
        return len(self.notas_calibradas()) / len(self.notas) if self.notas else 0.0

    # ── plantillas para el reconocedor ─────────────────────────────────
    def templates(self) -> dict[str, np.ndarray]:
        """{nota: vector 126}. Cacheado; se invalida al capturar/cargar."""
        if self._templates_cache is not None:
            return self._templates_cache
        refs = self.profile.references if self.profile else {}
        out: dict[str, np.ndarray] = {}
        for nota, snap in refs.items():
            vec = hands_to_vector(snap.get("hands", []))
            if vec.size == config.GESTURE_VECTOR_DIMS:
                out[nota] = vec
        self._templates_cache = out
        return out

    def classify(self, hands_data: list[dict]) -> str | None:
        """Atajo: reconoce la nota de una pose usando estas plantillas."""
        return GestureRecognizer(self).recognize(hands_data)

    # ── normalización (Fase 4: se hará automática y por escala) ────────
    @staticmethod
    def normalize(raw_landmarks: list[list[float]]) -> list[list[float]]:
        """Centra los 21 landmarks de una mano en su muñeca (landmark 0).
        MediaPipe entrega coordenadas absolutas; esto las hace relativas."""
        if not raw_landmarks:
            return []
        wx, wy, wz = raw_landmarks[0]
        return [[x - wx, y - wy, z - wz] for x, y, z in raw_landmarks]

    # ── persistencia ───────────────────────────────────────────────────
    def path(self) -> Path:
        return config.CALIBRATION_DIR / f"{self.user_id}.json"

    def load(self, fallback_to_referencia: bool = True) -> CalibrationProfile:
        """Carga la calibración del niño; si no existe y `fallback_to_referencia`,
        usa `pentagrama_calibrado.reference.json` (solo lectura)."""
        p = self.path()
        if p.exists():
            self.profile = CalibrationProfile.from_json(p.read_text(encoding="utf-8"))
        elif fallback_to_referencia and config.PENTAGRAMA_REFERENCIA.exists():
            ref = CalibrationProfile.from_json(
                config.PENTAGRAMA_REFERENCIA.read_text(encoding="utf-8")
            )
            ref.user_id = self.user_id
            self.profile = ref
        else:
            self.profile = CalibrationProfile(user_id=self.user_id, created_at=_now_iso())
        self._templates_cache = None
        return self.profile

    def save(self) -> None:
        """Persiste `self.profile` en data/calibration/<user_id>.json (atómico)."""
        if self.profile is None:
            raise RuntimeError("Nada que guardar: llama a iniciar()/capturar() primero.")
        self.path().parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path().with_suffix(".json.tmp")
        tmp.write_text(self.profile.to_json(), encoding="utf-8")
        tmp.replace(self.path())


# ── helpers de módulo ──────────────────────────────────────────────────
def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _as_list(landmarks) -> list[list[float]]:
    """Acepta list o np.ndarray y devuelve listas planas JSON-serializables."""
    if isinstance(landmarks, np.ndarray):
        return landmarks.tolist()
    return [list(map(float, lm)) for lm in landmarks]
