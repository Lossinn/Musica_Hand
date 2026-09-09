"""Descarga el modelo de landmarks de manos de MediaPipe (API Tasks, >= 1.0).

Solo hace falta si `mediapipe` no trae la API clásica `mp.solutions.hands`.
Alternativa sin descarga:  pip install 'mediapipe>=0.10.14,<0.11'

    python -m Prototipo.tools.descargar_modelo
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

from .. import config

URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)


def main() -> int:
    destino: Path = config.MODELS_DIR / "gesture" / "hand_landmarker.task"
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        print(f"Ya existe: {destino}")
        return 0
    print(f"Descargando {URL}\n  -> {destino}")
    urllib.request.urlretrieve(URL, destino)
    print(f"Listo ({destino.stat().st_size // 1024} KB).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
