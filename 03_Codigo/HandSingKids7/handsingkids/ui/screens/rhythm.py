"""Pantalla de juego de la mecánica de nota viajera: cámara + pista animada.

Una canción del catálogo cuenta para el progreso del niño exactamente igual
que un ejercicio guiado (pasa por `learning.session_flow.apply_result` y
termina en la pantalla de Resultados de siempre); una melodía grabada en
Modo Libre se juega y se puntúa aquí mismo, solo por diversión, sin tocar esa
contabilidad ni pasar por Resultados.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ...core.events import Event
from ...data import melodies
from ...domain.entities import Activity, ActivityKind, PlayMode
from ...learning.rhythm import TEMPO_FACTORS, TEMPO_LABELS, RhythmRunner
from ...learning.session_flow import apply_result
from .. import theme as T
from ..widgets.camera_view import CameraView
from ..widgets.rhythm_track import TravelingNoteTrack
from ..widgets.toy import (Body, Card, Chip, RoundIconButton, StarRow, Title,
                           ToyButton)
from .base import Screen

REFRESH_MS = 30


class RhythmScreen(Screen):
    def __init__(self, ctx, parent=None) -> None:
        super().__init__(ctx, parent)
        self.runner: RhythmRunner | None = None
        self._activity: Activity | None = None
        self._gaps: list[float] | None = None
        self._cuenta_para_progreso = True
        self._tempo_factor = 1.0

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(T.S.margin, 20, T.S.margin, 20)
        raiz.setSpacing(14)

        barra = QHBoxLayout()
        barra.setSpacing(12)
        self.b_salir = RoundIconButton("←", "danger", 56)
        self.b_salir.clicked.connect(self._salir)
        barra.addWidget(self.b_salir)

        caja = QVBoxLayout()
        caja.setSpacing(0)
        self.titulo = Title("Canción", 26)
        caja.addWidget(self.titulo)
        self.subtitulo = Body("", 14)
        caja.addWidget(self.subtitulo)
        host = QWidget()
        host.setLayout(caja)
        barra.addWidget(host)
        barra.addStretch(1)

        self.chip_puntaje = Chip("0 puntos", T.C.sun_soft)
        self.chip_combo = Chip("", T.C.bubblegum_soft)
        self.chip_precision = Chip("", T.C.mint_soft)
        barra.addWidget(self.chip_puntaje)
        barra.addWidget(self.chip_combo)
        barra.addWidget(self.chip_precision)

        self.b_espejo = RoundIconButton("⇄", "ghost", 56)
        self.b_espejo.setToolTip("Modo espejo")
        self.b_espejo.clicked.connect(self._alternar_espejo)
        self.b_repetir = RoundIconButton("↻", "warm", 56)
        self.b_repetir.setToolTip("Repetir desde el principio")
        self.b_repetir.clicked.connect(self._reiniciar)
        barra.addWidget(self.b_espejo)
        barra.addWidget(self.b_repetir)
        raiz.addLayout(barra)

        self.camara = CameraView(border=T.C.tangerine)
        raiz.addWidget(self.camara, 1)

        # Juicio de cada nota ("¡Perfecto!"/"¡Bien!"/"Vale"/"Fallada"), como
        # en el HUD de "Notas Rítmicas": aparece un instante sobre la pista y
        # se apaga solo, con el color de su categoría.
        self.etiqueta_juicio = Title("", 22)
        self.etiqueta_juicio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.etiqueta_juicio.setMinimumHeight(30)
        raiz.addWidget(self.etiqueta_juicio)

        self.pista = TravelingNoteTrack()
        raiz.addWidget(self.pista)

        # Tarjeta de cierre solo para las melodías grabadas: no hay pantalla
        # de Resultados que mostrar porque no se genera ningún intento real.
        self.tarjeta_fin = Card(bg=T.C.sun_soft, border=T.C.sun, padding=20)
        self.tarjeta_fin.setVisible(False)
        self.tarjeta_fin.body().addWidget(Title("¡Genial! 🎉", 26))
        self.estrellas_fin = StarRow(0, 3, 44)
        self.tarjeta_fin.body().addWidget(self.estrellas_fin)
        self.texto_fin = Body("", 16)
        self.tarjeta_fin.body().addWidget(self.texto_fin)
        acciones_fin = QHBoxLayout()
        b_otra = ToyButton("Otra vez", "secondary", "↻", height=64, font_size=17)
        b_otra.clicked.connect(self._reiniciar)
        b_volver = ToyButton("Volver a Canciones", "primary", "🎵",
                             height=64, font_size=17)
        b_volver.clicked.connect(lambda: self.go("songs"))
        acciones_fin.addWidget(b_otra)
        acciones_fin.addWidget(b_volver)
        self.tarjeta_fin.body().addLayout(acciones_fin)
        raiz.addWidget(self.tarjeta_fin)

        self._refresco = QTimer(self)
        self._refresco.setInterval(REFRESH_MS)
        self._refresco.timeout.connect(self.pista.refresh)

        self._flash_timer = QTimer(self)
        self._flash_timer.setSingleShot(True)
        self._flash_timer.timeout.connect(lambda: self.camara.set_flash(None))

        self._juicio_timer = QTimer(self)
        self._juicio_timer.setSingleShot(True)
        self._juicio_timer.timeout.connect(lambda: self.etiqueta_juicio.setText(""))

    # =================================================== ciclo de pantalla
    def on_enter(self, activity: Activity | None = None, melody=None,
                tempo_mode: str = "fijo", tempo_speed: str = "normal",
                **kwargs) -> None:
        if self.ctx.profile is None:
            self.go("profiles")
            return

        self._tempo_factor = TEMPO_FACTORS.get(tempo_speed, 1.0)
        self._gaps = None
        if activity is not None:
            self._activity = activity
            self._cuenta_para_progreso = True
            self.titulo.setText(activity.title)
            velocidad = ("" if tempo_speed == "normal"
                        else f" · {TEMPO_LABELS.get(tempo_speed, tempo_speed)}")
            self.subtitulo.setText(
                f"{activity.tempo_bpm} pulsos por minuto{velocidad} · "
                f"{T.format_duration(activity.duration_s)} · toca cuando la "
                f"nota llegue a la línea")
        elif melody is not None:
            self._cuenta_para_progreso = False
            self._activity = Activity(
                code=f"grabada_{melody.path.stem}", kind=ActivityKind.GAME,
                title="Tu melodía", level=0, difficulty=0.3, skill_codes=[],
                sequence=list(melody.notes), mode=PlayMode.MELODY,
                tempo_bpm=84, duration_s=max(20, int(melody.duration_s)),
                tolerance_ms=2200)
            self.titulo.setText("Tu melodía")
            if tempo_mode == "mi_ritmo":
                self._gaps = melodies.estimated_gaps_ms(melody)
                self.subtitulo.setText(
                    "A tu propio ritmo · toca cuando la nota llegue a la "
                    "línea · esto no queda guardado en tu progreso")
            else:
                self.subtitulo.setText(
                    "A tempo fijo · toca cuando la nota llegue a la línea · "
                    "esto no queda guardado en tu progreso")
        else:
            self.go("songs")
            return

        self.ctx.gestures.set_enabled(True)
        self.ctx.gestures.pause(False)
        self.ctx.gestures.frameReady.connect(self._on_frame)
        self._sub_conf = self.ctx.bus.subscribe(Event.GESTURE_CONFIRMED,
                                                self._on_confirmed)
        if not self.ctx.gestures.running:
            self.ctx.gestures.start()

        self._arrancar()

    def on_leave(self) -> None:
        self._refresco.stop()
        try:
            self.ctx.gestures.frameReady.disconnect(self._on_frame)
        except (RuntimeError, TypeError):
            pass
        if getattr(self, "_sub_conf", None):
            self._sub_conf()
        self.ctx.music.stop_playback()
        if self.runner and self.runner.running:
            self.runner.abandon()
        self.ctx.gestures.pause(True)

    # ========================================================= la partida
    def _arrancar(self) -> None:
        assert self._activity is not None
        if self.runner is not None:
            for señal in (self.runner.finished, self.runner.scoreChanged,
                         self.runner.noteJudged):
                try:
                    señal.disconnect()
                except (RuntimeError, TypeError):
                    pass
        self.runner = RhythmRunner(self._activity, self.ctx.profile.id,
                                   gaps_ms=self._gaps,
                                   tempo_factor=self._tempo_factor,
                                   bus=self.ctx.bus)
        self.runner.finished.connect(self._on_finished)
        self.runner.scoreChanged.connect(self._on_score)
        self.runner.noteJudged.connect(self._on_judged)
        self.pista.set_runner(self.runner)
        self.chip_puntaje.setText("0 puntos")
        self.chip_combo.setText("")
        self.chip_precision.setText("")
        self.etiqueta_juicio.setText("")
        self.tarjeta_fin.setVisible(False)
        self.camara.setVisible(True)
        self.pista.setVisible(True)
        self._refresco.start()
        QTimer.singleShot(500, self.runner.start)

    def _reiniciar(self) -> None:
        self.ctx.audio.button()
        if self.runner and self.runner.running:
            self.runner.abandon()
        self._arrancar()

    def _salir(self) -> None:
        self.ctx.audio.back()
        self.go("songs")

    # ------------------------------------------------------------ cámara
    def _on_frame(self, frame, hands) -> None:
        # Sin "barra de aceptación": la seña cuenta apenas se reconoce (ver
        # vision.stabilizer). La confirmación se ve en el flash de la
        # burbuja y se oye solo cuando la nota es la correcta.
        self.camara.set_frame(frame, hands, self.ctx.settings.vision.mirror)

    def _on_confirmed(self, message) -> None:
        if not self.runner or not self.runner.running:
            return
        nota = message.get("note")
        confianza = float(message.get("confidence", 0.0))
        # A diferencia del ejercicio guiado, aquí solo debe sonar la nota
        # correcta: si el niño hace otra seña (o la hace fuera de la ventana
        # de acierto de cualquier nota), `submit()` no hace sonar nada y,
        # calcando la mecánica original de "Notas Rítmicas", tampoco falla la
        # nota — sigue pendiente y el niño puede volver a intentarla hasta
        # que acierte o hasta que termine de cruzar la línea.
        if self.runner.submit(nota, confianza):
            self.ctx.music.trigger(nota, confianza)

    def _alternar_espejo(self) -> None:
        v = self.ctx.settings.vision
        v.mirror = not v.mirror
        self.ctx.settings.save()

    # ------------------------------------------------------------ juego
    def _on_score(self, puntaje: int, combo: int) -> None:
        self.chip_puntaje.setText(f"{puntaje} puntos")
        self.chip_combo.setText(f"⚡ {combo} seguidas" if combo >= 3 else "")

    # Colores y textos del juicio, calcados de "Notas Rítmicas" (Perfect =
    # verde, Good = azul, Ok = un tono cálido neutro, Miss = rojo), llevados
    # a la paleta de esta aplicación.
    _JUICIOS = {
        "perfecto": ("¡Perfecto!", T.C.mint, T.C.mint_bevel),
        "bien": ("¡Bien!", T.C.sky, T.C.sky_bevel),
        "vale": ("Vale", T.C.tangerine, T.C.tangerine_bevel),
    }

    def _on_judged(self, index: int, tipo: str, tier: str, offset_ms: int) -> None:
        if tipo == "acierto":
            texto, flash, color = self._JUICIOS.get(
                tier, ("Vale", T.C.tangerine, T.C.tangerine_bevel))
            self.camara.set_flash(flash, 0.22)
            duracion_juicio = 550
        else:
            texto, color = "Fallada", T.C.bubblegum_bevel
            self.camara.set_flash(T.C.bubblegum, 0.15)
            duracion_juicio = 700
        self.etiqueta_juicio.setText(texto)
        self.etiqueta_juicio.setStyleSheet(f"color: {color}; background: transparent;")
        self._juicio_timer.start(duracion_juicio)
        self._flash_timer.start(180)
        if self.runner:
            self.chip_precision.setText(f"🎯 {self.runner.live_accuracy:.0f}%")

    # ------------------------------------------------------------ cierre
    def _on_finished(self, result) -> None:
        self._refresco.stop()
        self.ctx.gestures.set_enabled(False)
        if self._cuenta_para_progreso:
            outcome = apply_result(self.ctx, self.runner)
            if outcome.stars_awarded or result.stars >= 3:
                self.ctx.audio.star()
            else:
                self.ctx.audio.applause()
            QTimer.singleShot(350, lambda: self.go(
                "results", outcome=outcome, activity=self._activity,
                cola=[], origen="rhythm"))
        else:
            if result.stars >= 3:
                self.ctx.audio.star()
            else:
                self.ctx.audio.applause()
            self.camara.setVisible(False)
            self.pista.setVisible(False)
            self.estrellas_fin.set_earned(result.stars)
            self.texto_fin.setText(
                f"Precisión {result.accuracy:.0f}% · {result.steps_correct}/"
                f"{result.steps_total} notas a tiempo · {result.score} "
                f"puntos. Esto fue solo por diversión: no queda guardado en "
                f"tu progreso.")
            self.tarjeta_fin.setVisible(True)
