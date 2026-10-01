#!/usr/bin/env python3
"""Punto de entrada de Hand Sing Kids."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _comprobar_entorno() -> list[str]:
    """Mensajes claros cuando falta algo, en lugar de una traza de error."""
    problemas: list[str] = []
    if sys.version_info < (3, 10):
        problemas.append(
            f"Se necesita Python 3.10 o superior; este es "
            f"{sys.version_info.major}.{sys.version_info.minor}.")
    if sys.version_info >= (3, 13):
        problemas.append(
            "MediaPipe todavía no publica versiones para Python 3.13. "
            "Usa Python 3.10, 3.11 o 3.12.")
    faltantes = []
    for modulo, paquete in (("PySide6", "PySide6"), ("cv2", "opencv-python"),
                            ("mediapipe", "mediapipe"), ("numpy", "numpy")):
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append(paquete)
    if faltantes:
        problemas.append("Faltan estos paquetes: " + ", ".join(faltantes)
                         + ".\n   Ejecuta:  pip install -r requirements.txt")
    return problemas


def main() -> int:
    problemas = _comprobar_entorno()
    if problemas:
        print("\n🎵 Hand Sing Kids no puede arrancar todavía:\n")
        for p in problemas:
            print(f" · {p}")
        print()
        return 1
    from handsingkids.app import run
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
