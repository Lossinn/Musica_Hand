"""Capa de persistencia (Fase 5).

Responsabilidad única: **leer y escribir JSON en disco de forma segura**.
Ningún módulo de dominio (auth, levels, composer, diagnostics) toca el sistema de
archivos directamente: todos pasan por un `JsonStore`. Así el resto del código es
testeable con un store en memoria y la ubicación de los datos es un detalle.

Estructura en disco (bajo `config.DATA_DIR`):

    users/<user_id>.json          perfil + credencial (hash)
    progress/<user_id>.json       ProgresoJugador (levels.py)
    diagnostics/<user_id>.json    Diagnostico (diagnostics.py)
    sessions/<user_id>/<ts>.json  registro de cada sesión
    calibration/<user_id>.json    CalibrationProfile (calibration.py)
    songs/<user_id>/<song_id>.json  Cancion (composer.py)
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from . import config

# Versión del esquema de datos en disco. Subir al romper compatibilidad;
# `migrar()` se encarga de traer datos viejos al esquema actual.
SCHEMA_VERSION = 1


class Store(Protocol):
    """Contrato mínimo de almacenamiento. `JsonStore` (disco) y
    `MemoryStore` (tests) lo implementan."""

    def leer(self, ruta: str) -> dict | None: ...
    def escribir(self, ruta: str, datos: dict) -> None: ...
    def existe(self, ruta: str) -> bool: ...
    def borrar(self, ruta: str) -> None: ...
    def listar(self, carpeta: str) -> list[str]: ...


@dataclass
class JsonStore:
    """Store respaldado por archivos JSON bajo `base_dir`.

    `ruta` es siempre relativa y con "/" (p. ej. "users/nino_01",
    "songs/nino_01/cancion_003"); la extensión .json la pone el store.
    """

    base_dir: Path = config.DATA_DIR

    def _path(self, ruta: str) -> Path:
        raise NotImplementedError("Fase 5: resolver ruta relativa -> Path .json (con guardas anti path-traversal)")

    def leer(self, ruta: str) -> dict | None:
        """Devuelve el dict guardado o None si no existe. Nunca lanza por
        ausencia; sí puede lanzar `PersistenceError` por JSON corrupto."""
        raise NotImplementedError("Fase 5: leer + json.loads + validar schema_version")

    def escribir(self, ruta: str, datos: dict) -> None:
        """Escritura atómica (archivo temporal + os.replace). Inyecta
        `_schema_version` y `_actualizado_en`."""
        raise NotImplementedError("Fase 5: escritura atómica de JSON")

    def existe(self, ruta: str) -> bool:
        raise NotImplementedError("Fase 5")

    def borrar(self, ruta: str) -> None:
        raise NotImplementedError("Fase 5")

    def listar(self, carpeta: str) -> list[str]:
        """IDs (sin .json) de los archivos directos de `carpeta`."""
        raise NotImplementedError("Fase 5: glob de *.json")


class MemoryStore:
    """Store en RAM para tests. Misma interfaz que `JsonStore`."""

    def __init__(self) -> None:
        self._data: dict[str, dict] = {}

    def leer(self, ruta: str) -> dict | None:
        return self._data.get(ruta)

    def escribir(self, ruta: str, datos: dict) -> None:
        self._data[ruta] = dict(datos)

    def existe(self, ruta: str) -> bool:
        return ruta in self._data

    def borrar(self, ruta: str) -> None:
        self._data.pop(ruta, None)

    def listar(self, carpeta: str) -> list[str]:
        pref = carpeta.rstrip("/") + "/"
        return sorted(
            k[len(pref):] for k in self._data
            if k.startswith(pref) and "/" not in k[len(pref):]
        )


class PersistenceError(Exception):
    """JSON corrupto, versión de esquema incompatible o escritura fallida."""


def migrar(datos: dict, destino: int = SCHEMA_VERSION) -> dict:
    """Trae un documento de un esquema viejo al `destino`. Idempotente."""
    raise NotImplementedError("Fase 5: cadena de migraciones por versión")


# Helpers de (de)serialización compartidos por los módulos de dominio.
def to_dict(obj: Any) -> dict:
    """dataclass anidada -> dict JSON-serializable (fechas ISO, Enums a str)."""
    raise NotImplementedError("Fase 5: dataclasses.asdict + normalización de tipos")


def from_dict(cls: type, datos: dict) -> Any:
    """Inverso de `to_dict` para una dataclass `cls` (tolerante a campos extra)."""
    raise NotImplementedError("Fase 5: reconstrucción de dataclass desde dict")
