"""Modo libre: tocar sin objetivo y guardar la melodía inventada."""

from __future__ import annotations

import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...core.events import Event
from ...domain.notes import NOTE_CODES, SILENCE
from .. import theme as T
from ..widgets.camera_view import CameraView
from ..widgets.notes import NoteBubble, NoteState, Staff
from ..widgets.toy import Body, Card, Chip, Title, ToyButton
from .base import Screen, header

MAX_NOTAS = 24


class FreePlayScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.melodia: list[str] = []
        self._inicio: float | None = None
        self._ultimo_evento: float | None = None
        self._gaps_ms: list[float] = []

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(T.S.margin, 20, T.S.margin, 20)
        raiz.setSpacing(14)

        self.chip = Chip("0 notas", T.C.violet_soft)
        self.chip_tiempo = Chip("0:00", T.C.sky_soft)
        raiz.addWidget(header("Crea tu melodía", on_back=lambda: self.go("home"),
                              subtitle="Haz las señas que quieras y quedará "
                                       "guardada tu canción",
                              extra=[self.chip, self.chip_tiempo]))

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)
        self.camara = CameraView(border=T.C.violet)
        cuerpo.addWidget(self.camara, 3)

        der = QVBoxLayout()
        der.setSpacing(12)
        tarjeta = Card(bg=T.C.white, padding=16)
        tarjeta.body().addWidget(Title("Tu melodía", 22))
        self.pentagrama = Staff([])
        tarjeta.body().addWidget(self.pentagrama)
        der.addWidget(tarjeta, 1)

        fila = QHBoxLayout()
        fila.setSpacing(8)
        self.burbujas = []
        for code in NOTE_CODES:
            b = NoteBubble(code, NoteState.PENDING, 44)
            self.burbujas.append(b)
            fila.addWidget(b)
        host = QWidget()
        host.setLayout(fila)
        der.addWidget(host)

        acciones = QHBoxLayout()
        acciones.setSpacing(10)
        b_escuchar = ToyButton("Escuchar", "secondary", "🔊", height=62,
                               font_size=17)
        b_escuchar.clicked.connect(self._escuchar)
        self.b_silencio = ToyButton("Silencio", "ghost", "🤫", height=62,
                                    font_size=17)
        self.b_silencio.setToolTip("Agrega una pausa a tu melodía")
        self.b_silencio.clicked.connect(self._agregar_silencio)
        b_borrar = ToyButton("Borrar", "danger", "🗑", height=62, font_size=17)
        b_borrar.clicked.connect(self._borrar)
        acciones.addWidget(b_escuchar)
        acciones.addWidget(self.b_silencio)
        acciones.addWidget(b_borrar)
        der.addLayout(acciones)

        self.b_guardar = ToyButton("Guardar mi canción", "success", "💾",
                                   height=70, font_size=19)
        self.b_guardar.clicked.connect(self._guardar)
        der.addWidget(self.b_guardar)
        cuerpo.addLayout(der, 2)
        raiz.addLayout(cuerpo, 1)

        self.mensaje = Body("", 16, T.C.mint_bevel)
        self.mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        raiz.addWidget(self.mensaje)

        self._reloj = QTimer(self)
        self._reloj.timeout.connect(self._actualizar_reloj)

    # ------------------------------------------------------------- ciclo
    def on_enter(self, **kwargs) -> None:
        if self.ctx.profile is None:
            self.go("profiles")
            return
        self.melodia = []
        self._inicio = None
        self._ultimo_evento = None
        self._gaps_ms = []
        self._refrescar()
        self.mensaje.setText("")
        self.ctx.gestures.set_enabled(True)
        self.ctx.gestures.pause(False)
        self.ctx.gestures.frameReady.connect(self._on_frame)
        self._sub = self.ctx.bus.subscribe(Event.GESTURE_CONFIRMED,
                                           self._on_confirmed)
        if not self.ctx.gestures.running:
            self.ctx.gestures.start()
        self._reloj.start(500)

    def on_leave(self) -> None:
        try:
            self.ctx.gestures.frameReady.disconnect(self._on_frame)
        except (RuntimeError, TypeError):
            pass
        if getattr(self, "_sub", None):
            self._sub()
        self.ctx.music.stop_playback()
        self.ctx.gestures.pause(True)
        self._reloj.stop()

    def _actualizar_reloj(self) -> None:
        transcurrido = (time.time() - self._inicio) if self._inicio else 0.0
        self.chip_tiempo.setText(T.format_duration(transcurrido))

    def _on_frame(self, frame, hands) -> None:
        # Sin "barra de aceptación": la seña cuenta apenas se reconoce (ver
        # vision.stabilizer); el flash de color al confirmar ya avisa qué
        # nota se grabó.
        self.camara.set_frame(frame, hands, self.ctx.settings.vision.mirror)

    def _on_confirmed(self, message) -> None:
        nota = message.get("note")
        if not nota or len(self.melodia) >= MAX_NOTAS:
            return
        if self._inicio is None:
            self._inicio = time.time()
        self.ctx.music.trigger(nota, float(message.get("confidence", 1.0)))
        self._registrar_intervalo()
        self.melodia.append(nota)
        self.camara.set_flash(T.NOTE_COLORS.get(nota, T.C.violet), 0.22)
        QTimer.singleShot(200, lambda: self.camara.set_flash(None))
        idx = NOTE_CODES.index(nota)
        self.burbujas[idx].set_state(NoteState.DONE)
        QTimer.singleShot(500,
                          lambda i=idx: self.burbujas[i].set_state(NoteState.PENDING))
        self._refrescar()

    def _agregar_silencio(self) -> None:
        """Agrega una pausa a la melodía: no viene de una seña, la elige el
        niño a propósito para dejar un espacio sin sonido."""
        if len(self.melodia) >= MAX_NOTAS:
            return
        if self._inicio is None:
            self._inicio = time.time()
        self.ctx.audio.button()
        self._registrar_intervalo()
        self.melodia.append(SILENCE)
        self._refrescar()

    def _registrar_intervalo(self) -> None:
        """Guarda cuánto pasó desde la nota (o silencio) anterior, en
        milisegundos. Es lo que permite reproducir la melodía "a mi ritmo"
        en el módulo Canciones, respetando el tiempo real que el niño dejó
        entre una seña y la siguiente en vez de repartir la duración total
        en partes iguales."""
        ahora = time.time()
        gap = (ahora - self._ultimo_evento) * 1000.0 if self._ultimo_evento else 0.0
        self._gaps_ms.append(gap)
        self._ultimo_evento = ahora

    def _refrescar(self) -> None:
        self.pentagrama.set_sequence(self.melodia)
        self.pentagrama.set_current(len(self.melodia) - 1)
        notas = sum(1 for c in self.melodia if c != SILENCE)
        silencios = len(self.melodia) - notas
        texto = f"{notas} notas"
        if silencios:
            texto += f" · {silencios} silencio(s)"
        self.chip.setText(texto)
        self.b_guardar.setEnabled(len(self.melodia) >= 3)

    def _escuchar(self) -> None:
        if self.melodia:
            self.ctx.music.play_sequence(self.melodia, 84)

    def _borrar(self) -> None:
        self.ctx.audio.back()
        self.melodia = []
        self._inicio = None
        self._ultimo_evento = None
        self._gaps_ms = []
        self._refrescar()
        self._actualizar_reloj()

    def _guardar(self) -> None:
        if len(self.melodia) < 3:
            return
        from ...data import melodies
        duracion = (time.time() - self._inicio) if self._inicio else 0.0
        melodies.save(self.ctx.profile.name, self.melodia, duracion,
                     gaps_ms=self._gaps_ms)
        self.ctx.achievements.unlock(self.ctx.profile.id, "compositor")
        self.ctx.audio.unlock()
        self.mensaje.setText(f"¡Guardada! Tu canción dura "
                             f"{T.format_duration(duracion)} y tiene "
                             f"{len(self.melodia)} notas 🎉 Búscala en "
                             f"Canciones para volver a tocarla.")
