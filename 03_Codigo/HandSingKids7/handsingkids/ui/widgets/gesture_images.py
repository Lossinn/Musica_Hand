"""Carga (con caché) las imágenes genéricas de las señas, si existen.

Una familia —o quien mantenga la aplicación— puede dejar sus propias
ilustraciones en `handsingkids/ui/assets/gestos/<CODIGO>.png` (también se
aceptan `.jpg`, `.jpeg` y `.webp`): una por nota, de DO3 a DO4. Son
ilustraciones genéricas, iguales para cualquier niño (a diferencia del dibujo
de la seña calibrada que ya existe en otras pantallas, que sale de las
muestras propias de cada niño). Si falta alguna imagen, o la carpeta entera
todavía no existe, la burbuja de esa nota simplemente muestra su color y su
nombre cantado, como ya ocurría antes de este módulo: nada se rompe por no
tener las imágenes todavía.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QPixmap

from ...core.config import ASSETS_DIR

GESTOS_DIR = Path(ASSETS_DIR) / "gestos"
_EXTS = (".png", ".jpg", ".jpeg", ".webp")
_cache: dict[str, QPixmap | None] = {}


def gesture_pixmap(code: str) -> QPixmap | None:
    """Devuelve la imagen genérica de la seña de `code`, o `None` si no hay
    ninguna todavía (no es un error: es el estado normal hasta que se agregan
    las ilustraciones)."""
    if code in _cache:
        return _cache[code]
    pix: QPixmap | None = None
    for ext in _EXTS:
        ruta = GESTOS_DIR / f"{code}{ext}"
        if ruta.exists():
            candidato = QPixmap(str(ruta))
            if not candidato.isNull():
                pix = candidato
            break
    _cache[code] = pix
    return pix


def reload_cache() -> None:
    """Limpia la caché en memoria. Útil tras agregar imágenes con la
    aplicación ya abierta, aunque lo normal es reiniciarla."""
    _cache.clear()


def missing_codes() -> list[str]:
    """Códigos de nota para los que todavía no hay imagen en disco. Se usa en
    Ajustes o en pantallas de diagnóstico para mostrarle a la familia qué
    falta, si algún día hace falta."""
    from ...domain.notes import NOTE_CODES
    return [c for c in NOTE_CODES if gesture_pixmap(c) is None]
