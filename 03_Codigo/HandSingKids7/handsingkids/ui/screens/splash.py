"""Pantalla de bienvenida."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...core.config import APP_VERSION
from .. import theme as T
from ..widgets.mascot import MascotView, Mood
from ..widgets.toy import Body, Title, ToyButton
from .base import Screen


class SplashScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(60, 40, 60, 40)
        lay.setSpacing(10)
        lay.addStretch(1)

        marca = QVBoxLayout()
        marca.setSpacing(2)
        titulo = Title("Hand Sing Kids", 64, T.C.on_surface)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lema = Body("🎵  Aprende música con tus manitas  🎵", 22, T.C.cocoa)
        lema.setAlignment(Qt.AlignmentFlag.AlignCenter)
        marca.addWidget(titulo)
        marca.addWidget(lema)
        contenedor = QWidget()
        contenedor.setLayout(marca)
        lay.addWidget(contenedor)

        self.mascota = MascotView(Mood.HAPPY, 260)
        fila = QHBoxLayout()
        fila.addStretch(1)
        fila.addWidget(self.mascota)
        fila.addStretch(1)
        lay.addLayout(fila)

        presentacion = Body("Soy Kiki y te voy a acompañar", 18,
                            T.C.on_surface_variant)
        presentacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(presentacion)
        lay.addSpacing(18)

        self.boton = ToyButton("Comenzar", "primary", "🚀", height=82,
                               font_size=26)
        self.boton.setMinimumWidth(320)
        self.boton.clicked.connect(self._comenzar)
        botones = QHBoxLayout()
        botones.addStretch(1)
        botones.addWidget(self.boton)
        botones.addStretch(1)
        lay.addLayout(botones)

        lay.addStretch(1)
        pie = Body(f"Versión {APP_VERSION} · Todo ocurre en este equipo: "
                   "la cámara no graba ni envía nada", 13, T.C.outline)
        pie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(pie)

    def on_enter(self, **kwargs) -> None:
        self.mascota.set_mood(Mood.HAPPY)
        self.ctx.audio.play_music("musica_inicio")

    def on_leave(self) -> None:
        self.ctx.audio.stop_music()

    def _comenzar(self) -> None:
        self.ctx.audio.button()
        self.ctx.audio.stop_music()
        self.mascota.celebrate(600)
        QTimer.singleShot(260, lambda: self.go("profiles"))
