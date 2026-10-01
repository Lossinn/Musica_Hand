"""Ajustes. Pensados para el adulto, no para el niño."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QSlider,
                               QVBoxLayout, QWidget)

from .. import theme as T
from ..widgets.toy import Body, Card, Title, ToyButton
from .base import Screen, header, page, scrollable


def fila(etiqueta: str, control: QWidget, ayuda: str = "") -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 6, 0, 6)
    lay.setSpacing(4)
    arriba = QHBoxLayout()
    arriba.addWidget(Body(etiqueta, 17, T.C.on_surface), 1)
    arriba.addWidget(control)
    lay.addLayout(arriba)
    if ayuda:
        lay.addWidget(Body(ayuda, 13, T.C.outline))
    return w


class SettingsScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        interior, self.lay = page()
        raiz.addWidget(scrollable(interior))

        self.lay.addWidget(header("Ajustes", on_back=lambda: self.go("home")))

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(18)

        # ---------------- cámara y reconocimiento ----------------
        camara = Card(bg=T.C.white, padding=20)
        camara.body().addWidget(Title("Cámara y reconocimiento", 22))

        self.combo_camara = QComboBox()
        for i in range(4):
            self.combo_camara.addItem(f"Cámara {i}", i)
        self.combo_camara.currentIndexChanged.connect(self._guardar)
        camara.body().addWidget(fila("Cámara", self.combo_camara,
                                     "Si la imagen no aparece, prueba otro número."))

        self.chk_espejo = QCheckBox()
        self.chk_espejo.stateChanged.connect(self._guardar)
        camara.body().addWidget(fila("Modo espejo", self.chk_espejo,
                                     "La imagen se ve como en un espejo."))

        self.chk_dos_manos = QCheckBox()
        self.chk_dos_manos.stateChanged.connect(self._guardar)
        camara.body().addWidget(fila("Exigir las dos manos", self.chk_dos_manos,
                                     "Desactívalo solo si calibraste con una."))

        self.sl_confianza = QSlider(Qt.Orientation.Horizontal)
        self.sl_confianza.setRange(30, 90)
        self.sl_confianza.valueChanged.connect(self._guardar)
        self.sl_confianza.setMinimumWidth(220)
        camara.body().addWidget(fila(
            "Exigencia del reconocedor", self.sl_confianza,
            "Más a la derecha, más seguro tiene que estar antes de aceptar una "
            "seña: menos notas por error, pero hay que hacerlas mejor."))

        self.sl_ventana = QSlider(Qt.Orientation.Horizontal)
        self.sl_ventana.setRange(1, 16)
        self.sl_ventana.valueChanged.connect(self._guardar)
        self.sl_ventana.setMinimumWidth(220)
        camara.body().addWidget(fila(
            "Tiempo de sostener la seña", self.sl_ventana,
            "En 1 (el valor de fábrica) la nota suena apenas se hace la seña, "
            "sin ninguna espera. Solo conviene subirlo si un niño en "
            "particular necesita más margen: entonces sí hay que sostener la "
            "seña varios fotogramas antes de que cuente."))

        self.b_recalibrar = ToyButton("Volver a calibrar las señas", "secondary",
                                      "📸", height=64, font_size=17)
        self.b_recalibrar.clicked.connect(
            lambda: self.go("calibration", primera_vez=False))
        camara.body().addWidget(self.b_recalibrar)
        cuerpo.addWidget(camara, 1)

        # ---------------- sonido y aprendizaje ----------------
        derecha = QVBoxLayout()
        derecha.setSpacing(16)

        sonido = Card(bg=T.C.white, padding=20)
        sonido.body().addWidget(Title("Sonido", 22))
        self.sl_general = QSlider(Qt.Orientation.Horizontal)
        self.sl_general.setRange(0, 100)
        self.sl_general.valueChanged.connect(self._guardar)
        sonido.body().addWidget(fila("Volumen general", self.sl_general))
        self.sl_musica = QSlider(Qt.Orientation.Horizontal)
        self.sl_musica.setRange(0, 100)
        self.sl_musica.valueChanged.connect(self._guardar)
        sonido.body().addWidget(fila("Notas musicales", self.sl_musica))
        self.sl_efectos = QSlider(Qt.Orientation.Horizontal)
        self.sl_efectos.setRange(0, 100)
        self.sl_efectos.valueChanged.connect(self._guardar)
        sonido.body().addWidget(fila("Efectos", self.sl_efectos))
        derecha.addWidget(sonido)

        aprendizaje = Card(bg=T.C.white, padding=20)
        aprendizaje.body().addWidget(Title("Aprendizaje", 22))
        self.sl_sesion = QSlider(Qt.Orientation.Horizontal)
        self.sl_sesion.setRange(3, 20)
        self.sl_sesion.valueChanged.connect(self._guardar)
        self.etiqueta_sesion = Body("", 13, T.C.outline)
        aprendizaje.body().addWidget(fila(
            "Duración de la sesión", self.sl_sesion,
            "Minutos que el motor usa como presupuesto al armar la ruta."))
        aprendizaje.body().addWidget(self.etiqueta_sesion)

        self.sl_actividades = QSlider(Qt.Orientation.Horizontal)
        self.sl_actividades.setRange(2, 8)
        self.sl_actividades.valueChanged.connect(self._guardar)
        aprendizaje.body().addWidget(fila("Actividades por ruta",
                                          self.sl_actividades))

        self.chk_adaptativo = QCheckBox()
        self.chk_adaptativo.stateChanged.connect(self._guardar)
        aprendizaje.body().addWidget(fila(
            "Adaptar la dificultad sola", self.chk_adaptativo,
            "Si se desactiva, las actividades se siguen en el orden del mapa."))

        self.chk_milp = QCheckBox()
        self.chk_milp.stateChanged.connect(self._guardar)
        aprendizaje.body().addWidget(fila(
            "Usar el optimizador", self.chk_milp,
            "Elige la ruta resolviendo un problema de optimización. Si se "
            "desactiva, se usa una selección rápida."))
        derecha.addWidget(aprendizaje)

        privacidad = Card(bg=T.C.mint_soft, border=T.C.mint, padding=18)
        privacidad.body().addWidget(Title("Privacidad", 20))
        privacidad.body().addWidget(Body(
            "La cámara se procesa solo en este equipo. No se guarda ninguna "
            "imagen ni vídeo: de la calibración solo se almacenan las "
            "coordenadas de los puntos de la mano. La aplicación no se conecta "
            "a internet y no muestra publicidad.", 15))
        derecha.addWidget(privacidad)
        derecha.addStretch(1)
        cuerpo.addLayout(derecha, 1)

        self.lay.addLayout(cuerpo, 1)
        self._cargando = False

    # -------------------------------------------------------------- ciclo
    def on_enter(self, **kwargs) -> None:
        self.ctx.gestures.pause(True)
        s = self.ctx.settings
        self._cargando = True
        self.combo_camara.setCurrentIndex(min(3, s.vision.camera_index))
        self.chk_espejo.setChecked(s.vision.mirror)
        self.chk_dos_manos.setChecked(s.vision.require_two_hands)
        self.sl_confianza.setValue(int(s.vision.confidence_threshold * 100))
        self.sl_ventana.setValue(s.vision.window_frames)
        self.sl_general.setValue(int(s.audio.master_volume * 100))
        self.sl_musica.setValue(int(s.audio.music_volume * 100))
        self.sl_efectos.setValue(int(s.audio.effects_volume * 100))
        self.sl_sesion.setValue(s.learning.session_minutes)
        self.sl_actividades.setValue(s.learning.activities_per_session)
        self.chk_adaptativo.setChecked(s.learning.adaptive)
        self.chk_milp.setChecked(s.learning.use_milp)
        self._cargando = False
        self._actualizar_etiquetas()

    def _actualizar_etiquetas(self) -> None:
        fps = max(1, self.ctx.settings.vision.target_fps)
        segundos = self.sl_ventana.value() / fps
        self.etiqueta_sesion.setText(
            f"Ruta de {self.sl_actividades.value()} actividades en "
            f"{self.sl_sesion.value()} minutos · sostener la seña "
            f"{segundos:.1f} s aproximadamente")

    def _guardar(self) -> None:
        if self._cargando:
            return
        s = self.ctx.settings
        s.vision.camera_index = int(self.combo_camara.currentData() or 0)
        s.vision.mirror = self.chk_espejo.isChecked()
        s.vision.require_two_hands = self.chk_dos_manos.isChecked()
        s.vision.confidence_threshold = self.sl_confianza.value() / 100.0
        s.vision.window_frames = self.sl_ventana.value()
        s.audio.master_volume = self.sl_general.value() / 100.0
        s.audio.music_volume = self.sl_musica.value() / 100.0
        s.audio.effects_volume = self.sl_efectos.value() / 100.0
        s.learning.session_minutes = self.sl_sesion.value()
        s.learning.activities_per_session = self.sl_actividades.value()
        s.learning.adaptive = self.chk_adaptativo.isChecked()
        s.learning.use_milp = self.chk_milp.isChecked()
        s.save()
        self.ctx.gestures.refresh_thresholds()
        self.ctx.optimizer.budget_minutes = s.learning.session_minutes
        self.ctx.optimizer.session_size = s.learning.activities_per_session
        self.ctx.optimizer.prefer_milp = s.learning.use_milp
        self._actualizar_etiquetas()
