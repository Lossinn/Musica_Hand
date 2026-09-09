"""Autenticación y perfiles del niño (Fases 5–6).

Flujo 1 del diseño ("Ingreso del niño"):
    Bienvenida -> [Ingresar | Crear perfil] -> se guarda el perfil para
    registrar y conservar el progreso.

Reglas:
  · La contraseña (a menudo un PIN corto para niños) se guarda SOLO como hash
    PBKDF2 con sal aleatoria. Nunca en texto plano, nunca en logs.
  · El `user_id` es estable y opaco (no es el nombre): el nombre se puede repetir
    o cambiar; el progreso se ancla al `user_id`.
  · `auth` no sabe de niveles ni de juego: solo identidad + datos básicos.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config
from .persistence import Store


@dataclass
class Perfil:
    """Datos del niño. Se serializa a `users/<user_id>.json`."""

    user_id: str
    nombre: str
    edad: int
    avatar: str = "pinguino"
    creado_en: str = ""
    ultima_sesion: str = ""
    # credencial — NUNCA se expone fuera de auth
    _password_hash: str = field(default="", repr=False)
    _salt: str = field(default="", repr=False)

    def publico(self) -> dict:
        """Vista sin credenciales, para pasar al resto de la app / UI."""
        return {
            "user_id": self.user_id,
            "nombre": self.nombre,
            "edad": self.edad,
            "avatar": self.avatar,
            "ultima_sesion": self.ultima_sesion,
        }


class AuthError(Exception):
    """Credenciales inválidas, nombre ya en uso, contraseña muy corta, etc.
    El mensaje es apto para mostrar a un niño ('Esa contraseña no coincide')."""


class AuthService:
    """Alta, login y logout. Usa un `Store` para persistir (Fase 5)."""

    def __init__(self, store: Store) -> None:
        self.store = store
        self.sesion: Perfil | None = None      # perfil autenticado actual

    # ── alta ────────────────────────────────────────────────────────────
    def crear_perfil(
        self,
        nombre: str,
        edad: int,
        password: str,
        avatar: str = "pinguino",
    ) -> Perfil:
        """Valida, crea el `user_id`, hashea la contraseña y persiste.

        Lanza `AuthError` si el nombre ya existe, la edad está fuera de
        `config.EDAD_MIN..MAX` o la contraseña es más corta que
        `config.PASSWORD_MIN_LEN`.
        """
        raise NotImplementedError("Fase 6: validación + alta de perfil")

    # ── login / logout ─────────────────────────────────────────────────
    def login(self, nombre: str, password: str) -> Perfil:
        """Verifica el hash y deja `self.sesion`. Lanza `AuthError` si falla."""
        raise NotImplementedError("Fase 6: verificación de credenciales")

    def logout(self) -> None:
        self.sesion = None

    # ── utilidades ─────────────────────────────────────────────────────
    def existe(self, nombre: str) -> bool:
        raise NotImplementedError("Fase 6: buscar por nombre en users/")

    def cambiar_password(self, user_id: str, actual: str, nueva: str) -> None:
        raise NotImplementedError("Fase 6")

    def perfiles(self) -> list[dict]:
        """Lista de vistas públicas — para una pantalla de 'elige tu perfil'."""
        raise NotImplementedError("Fase 6: listar users/ y devolver .publico()")

    # ── credencial (privado) ───────────────────────────────────────────
    @staticmethod
    def _hash(password: str, salt: str) -> str:
        """PBKDF2 (`config.PBKDF2_*`). Determinista dado (password, salt)."""
        raise NotImplementedError("Fase 6: hashlib.pbkdf2_hmac")

    @staticmethod
    def _nuevo_salt() -> str:
        raise NotImplementedError("Fase 6: secrets.token_hex")

    @staticmethod
    def _nuevo_user_id(nombre: str) -> str:
        """ID opaco y estable (p. ej. slug de nombre + sufijo aleatorio)."""
        raise NotImplementedError("Fase 6")
