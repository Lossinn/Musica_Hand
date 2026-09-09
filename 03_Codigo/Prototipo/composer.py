"""Editor de canciones (Fase 1 — parte de la app básica).

Flujo 4 del diseño ("Creación de canciones"), dos caminos:

  · **Modo Nivel X**: la paleta se restringe a las notas y figuras
    desbloqueadas hasta la etapa alcanzada (`curriculum.paleta_editor`).
  · **Modo Libre**: paleta completa, sin restricciones, con **grabación** de la
    interpretación gestual y **guardado**.

Una `Cancion` es una lista de `EventoCancion` con posición y duración en pulsos
(independiente del tempo), más metadatos. Se guarda en
`songs/<user_id>/<song_id>.json` y se puede reproducir con `pygame.mixer` usando
las frecuencias de las notas (ver 03_Codigo/Musica/notas.py cuando exista).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config, curriculum
from .persistence import Store


@dataclass
class EventoCancion:
    """Un sonido (o silencio) en la línea de tiempo de la canción."""

    figura: str                    # nombre de una curriculum.Figura
    nota: str | None = None        # None => silencio
    inicio_pulso: float = 0.0      # posición desde el comienzo, en pulsos de negra
    # duracion_pulsos se deriva de la figura, pero se guarda para robustez
    duracion_pulsos: float = 1.0


@dataclass
class Cancion:
    """Composición del niño. Serializable a `songs/<user_id>/<song_id>.json`."""

    song_id: str
    user_id: str
    titulo: str
    modo: str                      # "nivel" | "libre"
    etapa_id: int | None = None    # etapa activa al crearla (si modo == "nivel")
    compas: str = "4/4"
    bpm: int = 90
    eventos: list[EventoCancion] = field(default_factory=list)
    creada_en: str = ""
    duracion_s: float = 0.0
    origen: str = "editor"         # "editor" | "grabacion"

    def notas_usadas(self) -> set[str]:
        return {e.nota for e in self.eventos if e.nota}


class ComposerError(Exception):
    """Evento fuera de la paleta permitida, canción vacía al guardar, etc."""


class Editor:
    """Sesión de edición/grabación de UNA canción."""

    def __init__(
        self,
        store: Store,
        user_id: str,
        modo: str = "libre",
        etapa_id: int | None = None,
    ) -> None:
        self.store = store
        self.user_id = user_id
        self.modo = modo                       # "nivel" | "libre"
        self.etapa_id = etapa_id
        self.cancion: Cancion | None = None    # se crea en `nueva()`
        self._grabando: bool = False
        self._t0: float = 0.0                  # timestamp de inicio de grabación

    # ── paleta / validación (el "margen de acción" del editor) ──────────
    def paleta(self) -> dict:
        """Notas, figuras y compases disponibles según modo/etapa.
        Delega en `curriculum.paleta_editor`."""
        raise NotImplementedError("Fase 1: devolver curriculum.paleta_editor(etapa, modo)")

    def validar(self) -> list[str]:
        """Lista de problemas (vacía = canción válida): eventos fuera de paleta,
        solapamientos, compás incompleto, duración 0…"""
        raise NotImplementedError("Fase 1: validación de la canción contra la paleta")

    # ── edición manual ─────────────────────────────────────────────────
    def nueva(self, titulo: str = "Mi canción") -> Cancion:
        raise NotImplementedError("Fase 1: crear Cancion vacía con song_id nuevo")

    def agregar_evento(self, evento: EventoCancion) -> None:
        """Añade un evento; lanza `ComposerError` si la nota/figura no está en la
        paleta del modo actual."""
        raise NotImplementedError("Fase 1")

    def quitar_evento(self, indice: int) -> None:
        raise NotImplementedError("Fase 1")

    def mover_evento(self, indice: int, nuevo_inicio_pulso: float) -> None:
        raise NotImplementedError("Fase 1")

    # ── grabación de la interpretación gestual ─────────────────────────
    def iniciar_grabacion(self, bpm: int, compas: str = "4/4") -> None:
        """Arranca el reloj. A partir de aquí `registrar_gesto` cuantiza a la
        rejilla rítmica."""
        raise NotImplementedError("Fase 1: iniciar grabación con metrónomo")

    def registrar_gesto(self, nota: str, t_segundos: float) -> None:
        """Llega desde `vision`/`recognizer` durante la grabación: convierte el
        instante en `inicio_pulso` y estima la figura por el hueco al siguiente
        gesto (cuantización)."""
        raise NotImplementedError("Fase 1: cuantización gesto -> EventoCancion")

    def detener_grabacion(self) -> Cancion:
        """Cierra la grabación, cuantiza la última nota y devuelve la canción."""
        raise NotImplementedError("Fase 1")

    # ── reproducción ───────────────────────────────────────────────────
    def reproducir(self, cancion: Cancion | None = None) -> None:
        """Suena la canción (pygame.mixer) al `bpm` guardado."""
        raise NotImplementedError("Fase 1: síntesis/reproducción de la secuencia")

    # ── persistencia ───────────────────────────────────────────────────
    def guardar(self, titulo: str | None = None) -> Cancion:
        """Valida y persiste en `songs/<user_id>/<song_id>.json`. Incrementa
        `ProgresoJugador.total_canciones_creadas` a través del llamador."""
        raise NotImplementedError("Fase 1: validar + store.escribir")

    @staticmethod
    def cargar(store: Store, user_id: str, song_id: str) -> Cancion:
        raise NotImplementedError("Fase 1")

    @staticmethod
    def listar(store: Store, user_id: str) -> list[Cancion]:
        """Todas las canciones del niño — para la pantalla 'Canciones'."""
        raise NotImplementedError("Fase 1")

    @staticmethod
    def borrar(store: Store, user_id: str, song_id: str) -> None:
        raise NotImplementedError("Fase 1")
