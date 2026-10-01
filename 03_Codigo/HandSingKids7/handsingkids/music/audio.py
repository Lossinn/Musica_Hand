"""Reproducción de sonido.

Se usa QSoundEffect, que reproduce WAV con baja latencia: para un juego donde el
sonido debe llegar junto con el gesto, esto importa más que la calidad. Cada
sonido tiene un pequeño grupo de reproductores para que dos notas seguidas no se
corten entre sí.

Si el equipo no tiene salida de audio disponible, la aplicación sigue
funcionando en silencio en lugar de fallar.

Hay tres niveles de prioridad para cada sonido, de mayor a menor:

1. Lo que una familia deje en 'sonidos_personalizados', dentro de los datos de
   la aplicación (ver core.config.custom_audio_dir) — nunca se toca desde aquí.
2. Los sonidos reales incluidos con la propia aplicación en
   'handsingkids/ui/assets/audio/' (ver core.config.bundled_audio_dir) — por
   ejemplo, grabaciones reales de cada nota en vez del timbre sintético.
3. El sonido generado por síntesis (music.synth), que sirve de respaldo si
   falta cualquiera de los dos anteriores.

Si un nivel no tiene el archivo, simplemente se usa el siguiente: no hace
falta que estén completos los ocho para que la aplicación funcione.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QUrl

from ..core.config import (AudioSettings, audio_cache_dir, bundled_audio_dir,
                           custom_audio_dir)
from ..domain.notes import NOTE_CODES
from .synth import build_all

log = logging.getLogger(__name__)

VOICES_PER_SOUND = 3

# Nombres reconocidos en la carpeta de sonidos personalizados: uno por cada
# nota y uno por cada efecto/música que la aplicación reproduce.
LEEME_PERSONALIZADOS = """Sonidos personalizados de Hand Sing Kids
========================================

Para usar tus propios sonidos, deja aquí un archivo .wav con alguno de estos
nombres exactos (no hace falta ponerlos todos; los que falten siguen sonando
con la versión generada por la aplicación):

  nota_DO3.wav  nota_RE3.wav  nota_MI3.wav  nota_FA3.wav
  nota_SOL3.wav nota_LA3.wav  nota_SI3.wav  nota_DO4.wav
  acierto.wav      (al completar una actividad)
  casi.wav         (una seña casi correcta)
  estrella.wav     (al ganar tres estrellas)
  desbloqueo.wav   (al abrir una seña o logro nuevo)
  aplauso.wav      (al terminar sin llegar a tres estrellas)
  pulso.wav / pulso_fuerte.wav  (metrónomo)
  boton.wav / atras.wav         (botones)
  musica_inicio.wav             (música de la pantalla de bienvenida, en bucle)
  musica_fondo.wav              (música de fondo de las pantallas principales,
                                  en bucle — no suena mientras la cámara está
                                  activa: calibración, ejercicios, modo libre
                                  ni Canciones, para no tapar el sonido de las
                                  notas)

Formato recomendado: WAV, 44100 Hz, mono o estéreo. Vuelve a abrir la
aplicación después de agregar un archivo para que lo tome en cuenta.
"""


class AudioEngine(QObject):
    def __init__(self, settings: AudioSettings, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.available = True
        self._files: dict[str, Path] = {}
        self._pools: dict[str, list] = {}
        self._cursor: dict[str, int] = {}
        self._effect_cls = None
        self._music_fx = None
        self._music_name: str | None = None
        self._prepare()

    # ------------------------------------------------------------ montaje
    def _prepare(self) -> None:
        try:
            from PySide6.QtMultimedia import QSoundEffect
            self._effect_cls = QSoundEffect
        except Exception as exc:       # pragma: no cover
            log.warning("sin soporte de audio: %s", exc)
            self.available = False

        try:
            self._files = build_all(audio_cache_dir())
        except Exception as exc:       # pragma: no cover
            log.warning("no se pudieron generar los sonidos: %s", exc)
            self.available = False

        self._apply_bundled_defaults()
        self._apply_custom_overrides()

    def _apply_bundled_defaults(self) -> None:
        """Sonidos reales que vienen con la aplicación (por ejemplo,
        grabaciones de cada nota en vez del timbre sintético), con prioridad
        sobre lo sintetizado pero por debajo de lo que la familia deje en
        'sonidos_personalizados'. Cualquier archivo aquí puede introducir un
        nombre nuevo (no solo reemplazar uno existente): así una música de
        fondo para las pantallas principales, por ejemplo, no necesita
        generarse por síntesis para poder sonar."""
        try:
            carpeta = bundled_audio_dir()
            if not carpeta.is_dir():
                return
            for archivo in sorted(carpeta.iterdir()):
                if archivo.suffix.lower() == ".wav":
                    self._files[archivo.stem] = archivo
        except Exception as exc:       # pragma: no cover
            log.warning("no se pudieron aplicar los sonidos incluidos: %s", exc)

    def _apply_custom_overrides(self) -> None:
        """Si la familia dejó su propio .wav para algún sonido, se usa ese en
        lugar del generado. No es un error que la carpeta esté vacía: es el
        caso normal mientras nadie haya puesto sonidos propios."""
        try:
            carpeta = custom_audio_dir()
            leeme = carpeta / "LEEME.txt"
            if not leeme.exists():
                leeme.write_text(LEEME_PERSONALIZADOS, encoding="utf-8")
            for nombre in list(self._files):
                propio = carpeta / f"{nombre}.wav"
                if propio.exists():
                    self._files[nombre] = propio
        except Exception as exc:       # pragma: no cover
            log.warning("no se pudieron aplicar sonidos personalizados: %s", exc)

    def preload(self) -> None:
        """Crea los reproductores. Conviene llamarlo una vez al arrancar para
        que la primera nota no llegue tarde."""
        if not self.available or self._effect_cls is None:
            return
        for name in self._files:
            self._pool(name)

    def _pool(self, name: str) -> list:
        if name in self._pools:
            return self._pools[name]
        path = self._files.get(name)
        if path is None or self._effect_cls is None:
            self._pools[name] = []
            return []
        pool = []
        for _ in range(VOICES_PER_SOUND):
            fx = self._effect_cls(self)
            fx.setSource(QUrl.fromLocalFile(str(path)))
            pool.append(fx)
        self._pools[name] = pool
        self._cursor[name] = 0
        return pool

    # --------------------------------------------------------- reproducción
    def play(self, name: str, gain: float = 1.0, effect: bool = True) -> None:
        if not self.available:
            return
        pool = self._pool(name)
        if not pool:
            return
        idx = self._cursor.get(name, 0)
        fx = pool[idx]
        self._cursor[name] = (idx + 1) % len(pool)
        channel = self.settings.effects_volume if effect else self.settings.music_volume
        try:
            fx.setVolume(max(0.0, min(1.0, gain * channel * self.settings.master_volume)))
            fx.play()
        except Exception:               # pragma: no cover
            pass

    def play_note(self, code: str, gain: float = 1.0) -> None:
        if code in NOTE_CODES:
            self.play(f"nota_{code}", gain=gain, effect=False)

    # ------------------------------------------------------- música de fondo
    def play_music(self, name: str, gain: float = 0.6) -> None:
        """Reproduce una pista en bucle (p. ej. la música de bienvenida).

        A diferencia de play(), usa un único reproductor propio en lugar del
        turno rotativo de voces: una música de fondo no debe competir consigo
        misma ni cortarse cuando otro sonido pide el mismo canal.

        Llamar dos veces seguidas con el mismo nombre no reinicia la pista
        desde el principio: es lo que permite invocar esto en cada cambio de
        pantalla sin que la música de fondo dé un salto audible cada vez."""
        if self._music_name == name and self._music_fx is not None:
            return
        self.stop_music()
        if not self.available or self._effect_cls is None:
            return
        path = self._files.get(name)
        if path is None:
            return
        try:
            fx = self._effect_cls(self)
            fx.setSource(QUrl.fromLocalFile(str(path)))
            fx.setLoopCount(self._effect_cls.Infinite)
            fx.setVolume(max(0.0, min(1.0, gain * self.settings.music_volume *
                                      self.settings.master_volume)))
            fx.play()
            self._music_fx = fx
            self._music_name = name
        except Exception:               # pragma: no cover
            pass

    def stop_music(self) -> None:
        fx = getattr(self, "_music_fx", None)
        if fx is not None:
            try:
                fx.stop()
            except Exception:           # pragma: no cover
                pass
            self._music_fx = None
            self._music_name = None

    # Atajos con nombre, para que las pantallas no manejen cadenas sueltas.
    def correct(self) -> None: self.play("acierto")
    def almost(self) -> None: self.play("casi", gain=0.85)
    def star(self) -> None: self.play("estrella")
    def unlock(self) -> None: self.play("desbloqueo")
    def applause(self) -> None: self.play("aplauso")
    def tick(self, strong: bool = False) -> None:
        self.play("pulso_fuerte" if strong else "pulso", gain=0.7)
    def button(self) -> None: self.play("boton", gain=0.6)
    def back(self) -> None: self.play("atras", gain=0.6)

    def stop_all(self) -> None:
        self.stop_music()
        for pool in self._pools.values():
            for fx in pool:
                try:
                    fx.stop()
                except Exception:       # pragma: no cover
                    pass
