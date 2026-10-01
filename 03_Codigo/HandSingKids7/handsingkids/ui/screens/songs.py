"""Módulo Canciones: el catálogo de melodías completas y las que el niño ha
grabado en Modo Libre, todas jugables con la mecánica de nota viajera.

Las canciones del catálogo siguen existiendo también en el mapa de aventura,
donde se tocan paso a paso como cualquier otra actividad; aquí, en cambio, se
tocan con la nota viajando hacia la línea de impacto, y sí cuentan para el
dominio por nota y para el Agente Adaptativo (ver `ui.screens.rhythm`). Las
melodías grabadas en Modo Libre solo se tocan por diversión: no son parte del
catálogo pedagógico, así que no afectan esas estadísticas.
"""

from __future__ import annotations

import time

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...data import melodies
from ...domain.entities import ActivityKind
from .. import theme as T
from ..widgets.toy import Body, Card, Chip, Title, ToyButton
from .base import Screen, header, page, scrollable


class SongRow(Card):
    def __init__(self, activity, on_escuchar, on_jugar, parent=None) -> None:
        super().__init__(parent, bg=T.C.white, padding=14, radius=T.R.lg)
        fila = QHBoxLayout()
        fila.setSpacing(12)
        fila.addWidget(Title(activity.icon, 30))
        caja = QVBoxLayout()
        caja.setSpacing(2)
        caja.addWidget(Title(activity.title, 19))
        detalle = (f"{len(activity.sequence)} notas · {activity.tempo_bpm} bpm "
                  f"· ⏱ {T.format_duration(activity.duration_s)}")
        caja.addWidget(Body(detalle, 13))
        host = QWidget()
        host.setLayout(caja)
        fila.addWidget(host, 1)
        b_escuchar = ToyButton("Escuchar", "secondary", "🔊", height=52, font_size=15)
        b_escuchar.clicked.connect(lambda: on_escuchar(activity))
        fila.addWidget(b_escuchar)

        # Elegir el tiempo antes de jugar: la canción se siente "muy rápido"
        # para algunos niños, y un tempo más lento no solo alarga el
        # intervalo entre notas, también ensancha su ventana de acierto (ver
        # learning.rhythm.RhythmRunner.tempo_factor) — así aflojan de una
        # vez la velocidad y la exigencia.
        b_lento = ToyButton("🐢", "ghost", height=52, font_size=18)
        b_lento.setToolTip("Jugar más despacio")
        b_lento.clicked.connect(lambda: on_jugar(activity, "lento"))
        b_jugar = ToyButton("Jugar", "primary", "🎮", height=52, font_size=15)
        b_jugar.setToolTip("Jugar a tempo normal")
        b_jugar.clicked.connect(lambda: on_jugar(activity, "normal"))
        b_rapido = ToyButton("🐇", "ghost", height=52, font_size=18)
        b_rapido.setToolTip("Jugar más rápido")
        b_rapido.clicked.connect(lambda: on_jugar(activity, "rapido"))
        for b in (b_lento, b_jugar, b_rapido):
            fila.addWidget(b)
        self.body().addLayout(fila)


class RecordingRow(Card):
    def __init__(self, melodia, on_escuchar, on_jugar, parent=None) -> None:
        super().__init__(parent, bg=T.C.violet_soft, border=T.C.violet,
                         padding=14, radius=T.R.lg)
        fila = QHBoxLayout()
        fila.setSpacing(10)
        fila.addWidget(Title("🎼", 28))
        caja = QVBoxLayout()
        caja.setSpacing(2)
        fecha = time.strftime("%d/%m %H:%M", time.localtime(melodia.created_at))
        caja.addWidget(Title(f"Tu melodía del {fecha}", 17))
        detalle = f"{melodia.note_count} notas"
        if melodia.silence_count:
            detalle += f" · {melodia.silence_count} silencio(s)"
        detalle += f" · ⏱ {T.format_duration(melodia.duration_s)}"
        caja.addWidget(Body(detalle, 13))
        host = QWidget()
        host.setLayout(caja)
        fila.addWidget(host, 1)
        b_escuchar = ToyButton("Escuchar", "secondary", "🔊", height=52, font_size=14)
        b_escuchar.clicked.connect(lambda: on_escuchar(melodia))
        b_miritmo = ToyButton("A mi ritmo", "magic", "🎵", height=52, font_size=14)
        b_miritmo.setToolTip("Respeta el tiempo real entre nota y nota, "
                             "tal como la grabaste")
        b_miritmo.clicked.connect(lambda: on_jugar(melodia, "mi_ritmo"))
        b_fijo = ToyButton("Tempo fijo", "primary", "⏱", height=52, font_size=14)
        b_fijo.setToolTip("La toca a un pulso constante, como las del catálogo")
        b_fijo.clicked.connect(lambda: on_jugar(melodia, "fijo"))
        for b in (b_escuchar, b_miritmo, b_fijo):
            fila.addWidget(b)
        self.body().addLayout(fila)


class SongsScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.lay.addWidget(header(
            "Canciones", on_back=lambda: self.go("home"),
            subtitle="La nota viaja hasta la línea: hay que hacer la seña "
                     "justo cuando llega"))

        self.lay.addWidget(Title("Catálogo", 22))
        self.contenedor_catalogo = QVBoxLayout()
        self.contenedor_catalogo.setSpacing(10)
        self.lay.addLayout(self.contenedor_catalogo)

        fila_grabadas = QHBoxLayout()
        fila_grabadas.addWidget(Title("Tus melodías grabadas", 22), 1)
        fila_grabadas.addWidget(Chip("Modo Libre", T.C.violet_soft))
        self.lay.addLayout(fila_grabadas)
        self.mensaje_vacio = Body(
            "Todavía no has guardado ninguna melodía. Ve a «Crear melodía», "
            "en el inicio, para grabar la primera.", 15)
        self.lay.addWidget(self.mensaje_vacio)
        self.contenedor_grabadas = QVBoxLayout()
        self.contenedor_grabadas.setSpacing(10)
        self.lay.addLayout(self.contenedor_grabadas)
        self.lay.addStretch(1)

    # ------------------------------------------------------------- ciclo
    def on_enter(self, **kwargs) -> None:
        p = self.ctx.profile
        if p is None:
            self.go("profiles")
            return
        self.ctx.gestures.pause(True)

        self._limpiar(self.contenedor_catalogo)
        for a in self.ctx.activities.by_kind(ActivityKind.SONG):
            self.contenedor_catalogo.addWidget(
                SongRow(a, self._escuchar_catalogo, self._jugar_catalogo))

        self._limpiar(self.contenedor_grabadas)
        grabadas = melodies.list_for_profile(p.name)
        self.mensaje_vacio.setVisible(not grabadas)
        for m in grabadas:
            self.contenedor_grabadas.addWidget(
                RecordingRow(m, self._escuchar_grabada, self._jugar_grabada))

    def on_leave(self) -> None:
        self.ctx.music.stop_playback()

    @staticmethod
    def _limpiar(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # ------------------------------------------------------------ acciones
    def _escuchar_catalogo(self, activity) -> None:
        self.ctx.music.play_sequence(activity.sequence, activity.tempo_bpm)

    def _jugar_catalogo(self, activity, tempo_speed: str = "normal") -> None:
        self.ctx.audio.button()
        self.go("rhythm", activity=activity, tempo_speed=tempo_speed)

    def _escuchar_grabada(self, melodia) -> None:
        self.ctx.music.play_sequence(melodia.notes, 84)

    def _jugar_grabada(self, melodia, modo: str) -> None:
        self.ctx.audio.button()
        self.go("rhythm", melody=melodia, tempo_mode=modo)
